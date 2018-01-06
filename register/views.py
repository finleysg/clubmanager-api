import logging

import pytz
from datetime import timedelta
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from courses.models import CourseSetupHole
from core.models import Member, SeasonSettings
from events.models import Event
from .payments import stripe_charge, get_stripe_charges, get_stripe_charge
from .models import RegistrationGroup, RegistrationSlotPayment
from .serializers import RegistrationSlotSerializer, RegistrationGroupSerializer, RegistrationSlotPaymentSerializer
from .event_reservation import create_event
from .email import *

logger = logging.getLogger(__name__)
config = SeasonSettings.objects.current_settings()


@permission_classes((permissions.IsAuthenticated,))
class RegistrationGroupList(generics.ListCreateAPIView):
    """ API endpoint to view Registration Groups
    """
    serializer_class = RegistrationGroupSerializer

    def get_queryset(self):
        queryset = RegistrationGroup.objects.all()
        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            queryset = queryset.filter(event=event_id)
        return queryset


@permission_classes((permissions.IsAuthenticated,))
class RegistrationGroupDetail(generics.RetrieveAPIView):
    """ API endpoint to view Registration Groups
    """
    queryset = RegistrationGroup.objects.all()
    serializer_class = RegistrationGroupSerializer


@permission_classes((permissions.AllowAny,))
class RegistrationList(generics.ListAPIView):

    serializer_class = RegistrationSlotSerializer

    def get_queryset(self):
        """
        Optionally restricts the list of registrations for a given event.
        """
        queryset = RegistrationSlot.objects.all()
        event_id = self.request.query_params.get('event_id', None)
        member_id = self.request.query_params.get('member_id', None)
        is_open = self.request.query_params.get('is_open', False)
        if event_id is not None:
            queryset = queryset.filter(event=event_id)
        if member_id is not None:
            queryset = queryset.filter(member=member_id)
        if is_open:
            queryset = queryset.filter(member__isnull=True)
        return queryset


@permission_classes((permissions.IsAuthenticated,))
class RegistrationDetail(generics.RetrieveUpdateAPIView):
    queryset = RegistrationSlot.objects.all()
    serializer_class = RegistrationSlotSerializer


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def get_charge(request):
    charge_id = request.query_params.get('id', None)
    charge_detail = get_stripe_charge(charge_id)
    return Response(charge_detail)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def get_charges(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_charges = get_stripe_charges(event)
    return Response(event_charges)


@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def is_registered(request, event_id, member_id):
    result = RegistrationSlot.objects.is_registered(event_id, member_id)
    return Response({'registered': result}, status=200)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def reserve(request):

    # Is an admin registering a member?
    member_id = request.data.get("member_id", request.user.member.id)
    member = Member.objects.get(pk=member_id)
    registrar = Member.objects.get(pk=request.user.member.id)

    event_id = request.data.get("event_id", 0)
    if event_id == 0:
        raise ValidationError("There was no event id passed")

    event = Event.objects.filter(pk=event_id).get()
    if event is None:
        raise ValidationError("{} is not a valid event id".format(event_id))

    if event.registration_window() != "registration" and not request.user.is_staff:
        raise ValidationError("Event {} is not open for registration".format(event_id))

    course_setup_hole_id = request.data.get("course_setup_hole_id", None)
    if event.event_type == "L" and course_setup_hole_id is None:
        raise ValidationError("A hole id is required for weekday evening events")

    slot_ids = request.data.get("slot_ids", None)
    if event.event_type == "L" and slot_ids is None:
        raise ValidationError("At least one registration slot is required for weekday evening events")

    starting_order = request.data.get("starting_order", 0)

    reg_event = create_event(event)
    group = reg_event.reserve(registrar, member, **{
        "slot_ids": slot_ids,
        "course_setup_hole_id": course_setup_hole_id,
        "starting_order": starting_order
    })

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'PUT', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def register(request):

    group_tmp = request.data.get("group", None)
    if group_tmp is None:
        raise ValidationError("You neglected to submit a registration group")

    event = Event.objects.filter(pk=group_tmp["event"]).get()
    if event is None:
        raise ValidationError("{} is not a valid event id".format(group_tmp["event"]))

    group = RegistrationGroup.objects.filter(pk=group_tmp["id"]).get()
    if group is None:
        raise ValidationError("{} is not a valid group id".format(group_tmp["id"]))

    amount_due = float(group_tmp["payment_amount"])

    if request.method == "POST":
        group = register_new(request, event, group_tmp, group, amount_due)
    else:
        group = register_update(request, event, group_tmp, group, amount_due)

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


def register_new(request, event, group_tmp, group, amount_due):

    payment_code = group_tmp["payment_confirmation_code"]

    if payment_code == "Cash" or payment_code == "cash":
        group.payment_confirmation_code = "Cash"
        group.payment_amount = amount_due
        group.payment_confirmation_timestamp = tz.now()
    else:
        verification_token = group_tmp["card_verification_token"]
        if verification_token is None or verification_token == "":
            verification_token = "no-token"

        charge = stripe_charge(request.user, event, int(amount_due * 100), verification_token)

        group.payment_amount = amount_due
        group.card_verification_token = verification_token
        group.payment_confirmation_code = charge.id
        group.payment_confirmation_timestamp = tz.now()
        group.notes = group_tmp["notes"]

    group.save()

    for slot_tmp in group_tmp["slots"]:

        if type(slot_tmp["member"]) is dict:
            member_id = slot_tmp["member"]["id"]
        else:
            member_id = slot_tmp["member"]

        if member_id > 0:
            member = Member.objects.get(pk=member_id)
            RegistrationSlot.objects\
                .select_for_update()\
                .filter(pk=slot_tmp["id"])\
                .update(**{
                    "member": member,
                    "status": "R",
                    "is_event_fee_paid": slot_tmp.get("is_event_fee_paid", True),
                    "is_gross_skins_paid": slot_tmp.get("is_gross_skins_paid", False),
                    "is_net_skins_paid": slot_tmp.get("is_net_skins_paid", False),
                    "is_greens_fee_paid": slot_tmp.get("is_greens_fee_paid", False),
                    "is_cart_fee_paid": slot_tmp.get("is_cart_fee_paid", False)
                })
        else:
            RegistrationSlot.objects.select_for_update().filter(pk=slot_tmp["id"]).update(**{"status": "A"})

    # notification and confirmation/welcome emails
    if group.event == config.reg_event:
        if request.user.date_joined.year == config.year:
            send_new_member_notification(request.user, group, config)
            send_new_member_welcome(request.user, config)
        else:
            send_returning_member_welcome(request.user, config)
            send_has_notes_notification(request.user, group, event)
    elif group.event == config.match_play_event:
        send_event_confirmation(request.user, group, event, config)
    elif payment_code == "Cash" or payment_code == "cash":
        pass
    else:
        send_event_confirmation(request.user, group, event, config)
        send_has_notes_notification(request.user, group, event)

    return RegistrationGroup.objects.get(pk=group.id)


# updates support online skins only at this time
def register_update(request, event, group_tmp, group, amount_due):

    # allow a 10 minute grace period on the deadline
    skins_end = pytz.utc.normalize(event.skins_end)
    padded_now = tz.now() - timedelta(minutes=10)
    if padded_now > skins_end:
        raise ValidationError("Sorry, online skins registration has closed")

    payment_code = group_tmp["payment_confirmation_code"]
    verification_token = group_tmp["card_verification_token"]
    registrar = Member.objects.get(pk=request.user.member.id)
    payment_ts = tz.now()

    if payment_code != "Cash" or payment_code != "cash":
        if verification_token is None or verification_token == "":
            verification_token = "no-token"
        charge = stripe_charge(request.user, event, int(amount_due * 100), verification_token)
        payment_code = charge.id

    for slot_tmp in group_tmp["slots"]:
        RegistrationSlot.objects\
            .select_for_update()\
            .filter(pk=slot_tmp["id"])\
            .update(**{
                "is_gross_skins_paid": slot_tmp.get("is_gross_skins_paid", False),
                "is_net_skins_paid": slot_tmp.get("is_net_skins_paid", False),
                "is_greens_fee_paid": slot_tmp.get("is_greens_fee_paid", False),
                "is_cart_fee_paid": slot_tmp.get("is_cart_fee_paid", False)
            })
        # slot payment records repeat the payment info for each updated reg slot,
        # so that will have to be accounted for at reporting time
        slot = RegistrationSlot.objects.get(pk=slot_tmp["id"])
        slot_payment = RegistrationSlotPayment(
            registration_slot=slot,
            recorded_by=registrar,
            card_verification_token=verification_token,
            payment_code=payment_code,
            payment_timestamp=payment_ts,
            payment_amount=amount_due,
            comment="online skins"
        )
        slot_payment.save()

    # notification and confirmation/welcome emails
    # if group_tmp["payment_confirmation_code"] == "Cash":
    #     pass
    # else:
    #     send_event_confirmation(request.user, group, event, config)

    return RegistrationGroup.objects.get(pk=group.id)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def cancel_reserved_slots(request):

    group_id = request.data.get("group_id", 0)
    if group_id == 0:
        raise ValidationError("Missing group id")

    try:
        group = RegistrationGroup.objects.filter(pk=group_id).get()

        if len(group.payment_confirmation_code) > 0 and not request.user.is_staff:
            raise ValidationError("Cannot cancel a group that has already paid")

        if group.event.event_type == "L":
            RegistrationSlot.objects.filter(registration_group=group) \
                .update(**{"status": "A", "registration_group": None, "member": None})
        else:
            RegistrationSlot.objects.filter(registration_group=group).delete()

        group.delete()

    except ObjectDoesNotExist:
        # I hope if we sink this we improve the user experience (no red message) and don't cause any DB harm
        # Why would we ever get to here is a mystery -- maybe double click from the UI?
        logger.warning("Could not find and cancel a registration group with id {}".format(group_id), request=request)

    return Response(status=204)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def add_groups(request):

    event_id = request.data["event_id"]
    event = get_object_or_404(Event, pk=event_id)

    # select all the holes with only one group
    holes = list(RegistrationSlot.objects.filter(event=event)
                 .distinct()
                 .values_list("course_setup_hole", flat=True)
                 .annotate(row_count=Count("course_setup_hole"))
                 .filter(row_count__lte=event.group_size)
                 .order_by("course_setup_hole"))

    for hole in holes:
        instance = CourseSetupHole.objects.get(pk=hole)
        RegistrationSlot.objects.add_slots(event, instance)

    return Response({"groups_added": len(holes)}, status=201)

#
# @api_view(['POST', ])
# @permission_classes((permissions.IsAuthenticated,))
# @transaction.atomic()
# def remove_row(request):
#
#     event_id = request.data["event_id"]
#     course_setup_hole_id = request.data["course_setup_hole_id"]
#     starting_order = request.data["starting_order"]
#     event = get_object_or_404(Event, pk=event_id)
#     hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)
#
#     RegistrationSlot.objects.remove_hole(event, hole, starting_order)
#
#     return Response(status=204)


@permission_classes((permissions.IsAuthenticated,))
class RegistrationSlotPaymentList(generics.ListCreateAPIView):
    """ API endpoint to view Registration Slot Payments
    """
    serializer_class = RegistrationSlotPaymentSerializer

    def get_queryset(self):
        queryset = RegistrationSlotPayment.objects.all()
        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            queryset = queryset.filter(registration_slot__event=event_id)
            return queryset


@permission_classes((permissions.IsAuthenticated,))
class RegistrationSlotPaymentDetail(generics.RetrieveUpdateAPIView):
    """ API endpoint to view Registration Slot Payments
    """
    queryset = RegistrationSlotPayment.objects.all()
    serializer_class = RegistrationSlotPaymentSerializer
