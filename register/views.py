from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from courses.models import CourseSetupHole
from core.models import Member
from events.models import Event
from .payments import get_stripe_charges, get_stripe_charge
from .models import RegistrationGroup, RegistrationSlotPayment, RegistrationSlot
from .serializers import RegistrationSlotSerializer, RegistrationGroupSerializer, RegistrationSlotPaymentSerializer
from .utils import create_event, register_new, register_update


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
    group = RegistrationGroup.objects.filter(pk=group_tmp["id"]).get()

    amount_due = float(group_tmp.get("payment_amount", 0.0))
    payment_code = group_tmp.get("payment_confirmation_code", "cash")
    verification_token = group_tmp.get("card_verification_token", "no-token")
    if not verification_token:
        verification_token = "no-token"

    if request.method == "POST":
        group = register_new(request.user, event, group_tmp, group, amount_due, payment_code, verification_token)
    else:
        group = register_update(request.user, event, group_tmp, group, amount_due, payment_code, verification_token)

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


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
