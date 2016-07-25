from datetime import datetime, timedelta
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from events.models import Event
from courses.models import CourseSetupHole
from signup.models import SignupSlot, RegistrationGroup
from signup.serializers import SignupSlotSerializer


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def registration_slots(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    slots = SignupSlot.objects.filter(event=event)
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
        slot.save()

    # TODO: how can we return the new group id, too? or will it be on the slot records?
    serializer = SignupSlotSerializer(slots, context={'request': request}, many=True)
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
