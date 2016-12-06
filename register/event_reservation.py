from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import APIException

from courses.models import CourseSetupHole
from .exceptions import SlotConflictError, EventFullError
from .models import RegistrationSlot, RegistrationGroup


def create_event(event):

    if not event.requires_registration:
        raise APIException("{} does not require registration".format(event.name))

    if event.event_type == "L":
        return LeagueEvent(event)
    elif event.event_type == "W" and event.can_signup_group:
        return WeekendGroupEvent(event)
    else:
        return IndividualEvent(event)


class LeagueEvent:

    def __init__(self, event):
        self.event = event

    def reserve(self, member, slot_ids=None, course_setup_hole_id=None, starting_order=0):

        hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)
        slots = RegistrationSlot.objects.filter(pk__in=slot_ids)

        for slot in slots:
            if slot.status != "A":
                raise SlotConflictError()

        group = RegistrationGroup(event=self.event, course_setup=hole.course_setup, signed_up_by=member,
                                  starting_hole=hole.hole_number, starting_order=starting_order)
        group.save()

        for i, slot in enumerate(slots):
            slot.status = "P"
            slot.registration_group = group
            slot.course_setup_hole = hole
            slot.expires = timezone.now() + timedelta(minutes=10)
            if i == 0:
                slot.member = member
            slot.save()

        return group


class WeekendGroupEvent:

    def __init__(self, event):
        self.event = event

    def reserve(self, member, slot_ids=None, course_setup_hole_id=None, starting_order=0):

        if self.event.registration_maximum != 0:
            registrations = RegistrationSlot.objects.filter(event=self.event).count()
            if registrations >= self.event.registration_maximum:
                raise EventFullError()

        group = RegistrationGroup(event=self.event, course_setup=None, signed_up_by=member,
                                  starting_hole=1, starting_order=starting_order)
        group.save()

        for s in range(0, self.event.maximum_signup_group_size):
            slot = RegistrationSlot(event=self.event, starting_order=starting_order, slot=s)
            slot.status = "P"
            slot.registration_group = group
            slot.expires = timezone.now() + timedelta(minutes=10)
            if s == 0:
                slot.member = member
            slot.save()

        return group


class IndividualEvent:

    def __init__(self, event):
        self.event = event

    def reserve(self, member, slot_ids=None, course_setup_hole_id=None, starting_order=0):

        if self.event.registration_maximum != 0:
            registrations = RegistrationSlot.objects.filter(event=self.event).count()
            if registrations >= self.event.registration_maximum:
                raise EventFullError()

        group = RegistrationGroup(event=self.event, course_setup=None, signed_up_by=member,
                                  starting_hole=1, starting_order=starting_order)
        group.save()

        slot = RegistrationSlot(event=self.event, starting_order=starting_order, slot=0)
        slot.status = "P"
        slot.registration_group = group
        slot.expires = timezone.now() + timedelta(minutes=10)
        slot.member = member
        slot.save()

        return group
