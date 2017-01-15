from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from courses.models import CourseSetupHole
from core.models import Member
from events.models import Event
from .payments import stripe_charge
from .models import RegistrationSlot, RegistrationGroup
from .serializers import RegistrationSlotSerializer, RegistrationGroupSerializer
from .event_reservation import create_event
from .email import *


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
        if event_id is not None:
            queryset = queryset.filter(event=event_id)
        if member_id is not None:
            queryset = queryset.filter(member=member_id)
        return queryset


@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def is_registered(request, event_id, member_id):
    result = RegistrationSlot.objects.is_registered(event_id, member_id)
    return Response({'registered': result}, status=200)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def reserve(request):

    member = Member.objects.filter(pk=request.user.member.id).get()

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
        raise ValidationError("A hole id is required for league events")

    slot_ids = request.data.get("slot_ids", None)
    if event.event_type == "L" and slot_ids is None:
        raise ValidationError("At least one registration slot is required for league events")

    starting_order = request.data.get("starting_order", 0)

    reg_event = create_event(event)
    group = reg_event.reserve(member, **{
        "slot_ids": slot_ids,
        "course_setup_hole_id": course_setup_hole_id,
        "starting_order": starting_order
    })

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
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

        member = Member.objects.get(pk=slot_tmp["member"])
        if member is None:
            raise ValidationError("{} is an invalid member id".format(slot_tmp["member"]))

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

    # notification and welcome emails for new members
    if "NEW MEMBER" in group.notes:
        send_new_member_notification(request.user, group)

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def cancel_reserved_slots(request):

    group_id = request.data.get("group_id", 0)
    if group_id == 0:
        raise ValidationError("Missing group id")

    group = RegistrationGroup.objects.filter(pk=group_id).get()
    if group is None:
        raise ValidationError("{} is an invalid group id".format(group_id))

    if len(group.payment_confirmation_code) > 0 and not request.user.is_staff:
        raise ValidationError("Cannot cancel a group that has already paid")

    if group.event.event_type == "L":
        RegistrationSlot.objects.filter(registration_group=group) \
            .update(**{"status": "A", "registration_group": None, "member": None})
    else:
        RegistrationSlot.objects.filter(registration_group=group).delete()

    group.delete()

    return Response(status=204)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def add_row(request):

    event_id = request.data["event_id"]
    course_setup_hole_id = request.data["course_setup_hole_id"]
    event = get_object_or_404(Event, pk=event_id)
    hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)

    new_slots = RegistrationSlot.objects.add_slots(event, hole)

    serializer = RegistrationSlotSerializer(new_slots, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def remove_row(request):

    event_id = request.data["event_id"]
    course_setup_hole_id = request.data["course_setup_hole_id"]
    starting_order = request.data["starting_order"]
    event = get_object_or_404(Event, pk=event_id)
    hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)

    RegistrationSlot.objects.remove_hole(event, hole, starting_order)

    return Response(status=204)
