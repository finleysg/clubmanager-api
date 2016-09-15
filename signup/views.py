from datetime import datetime, timedelta
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.models import Member
from events.models import Event
from courses.models import CourseSetupHole
from signup.models import SignupSlot, RegistrationGroup, Registration
from signup.serializers import SignupSlotSerializer, RegistrationGroupSerializer


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def registration_slots(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    slots = SignupSlot.objects.filter(event=event)
    # TODO: how to guarantee single entry (i.e. run exactly once)
    if len(slots) == 0:
        slots = SignupSlot.objects.create_slots(event)

    serializer = SignupSlotSerializer(slots, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def reserve_slots(request):

    course_setup_hole_id = request.data["course_setup_hole_id"]
    slot_ids = request.data["slot_ids"]
    starting_order = request.data["starting_order"]
    event_id = request.data["event_id"]

    member = get_object_or_404(Member, pk=request.user.id)
    event = get_object_or_404(Event, pk=event_id)
    hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)
    slots = SignupSlot.objects.filter(pk__in=slot_ids)
    for slot in slots:
        if slot.status != "A":
            return HttpResponseBadRequest("One or more of the signup slots you requested are no longer available.")

    group = RegistrationGroup(event=event, course_setup=hole.course_setup, signed_up_by=request.user.member,
                              starting_hole=hole.hole_number, starting_order=starting_order)
    group.save()

    for slot in slots:
        slot.status = "P"
        slot.registration_group = group
        slot.course_setup_hole = hole
        slot.expires = datetime.now() + timedelta(minutes=10)
        if slot.slot == 0:
            slot.member = member
        slot.save()

    # TODO: Do I need to do this?
    # group = get_object_or_404(RegistrationGroup, pk=group.id)

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def register(request):
    group_tmp = request.data["group"]

    group = get_object_or_404(RegistrationGroup, pk=group_tmp["id"], signed_up_by=request.user.member)
    group.payment_amount = group_tmp["payment_amount"];
    group.save()

    for slot_tmp in group_tmp["slots"]:
        slot = SignupSlot.objects.get(pk=slot_tmp["id"])
        member = Member.objects.get(pk=slot_tmp["member"])
        slot.status = "R"
        slot.member = member
        slot.save()
        registration = Registration(registration_group=group, member=member,
                                    is_event_fee_paid=slot_tmp["include_event_fee"],
                                    is_gross_skins_paid=slot_tmp["include_gross_skins"],
                                    is_net_skins_paid=slot_tmp["include_skins"])
        registration.save()

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def cancel_reserved_slots(request, registration_group_id):

    group = get_object_or_404(RegistrationGroup, pk=registration_group_id, signed_up_by=request.user)
    slots = SignupSlot.objects.filter(registration_group=group)

    for slot in slots:
        slot.status = "A"
        slot.registration_group = None
        slot.course_setup_hole = None
        slot.expires = None
        slot.save()

    group.delete()

    serializer = SignupSlotSerializer(slots, context={'request': request}, many=True)
    return Response(serializer.data)
