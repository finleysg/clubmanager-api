import logging

from datetime import timedelta
from django.utils import timezone
from rest_framework.serializers import ValidationError

from courses.models import CourseSetupHole
from .exceptions import EventFullError, SlotConflictError
from .models import RegistrationSlot, RegistrationGroup


def create_event(event):

    if not event.requires_registration:
        raise ValidationError("{} does not require registration".format(event.name))

    if event.event_type == "L":
        return LeagueEvent(event)
    # elif event.event_type == "W" and event.can_signup_group:
    #     return WeekendGroupEvent(event)
    else:
        return NonLeagueEvent(event)


class LeagueEvent:

    def __init__(self, event):
        self.event = event
        self.logger = logging.getLogger(__name__)

    def reserve(self, registrar, member, slot_ids=None, course_setup_hole_id=None, starting_order=0):

        hole = CourseSetupHole.objects.filter(pk=course_setup_hole_id).get()
        if hole is None:
            raise ValidationError("Hole id {} is not valid".format(course_setup_hole_id))

        group = RegistrationGroup(event=self.event, course_setup=hole.course_setup, signed_up_by=registrar,
                                  starting_hole=hole.hole_number, starting_order=starting_order)
        group.expires = timezone.now() + timedelta(minutes=10)
        group.save()

        self.logger.info("selecting slots for update for member {} and group {}".format(member.id, group.id))
        slots = list(RegistrationSlot.objects.select_for_update().filter(pk__in=slot_ids))
        for s in slots:
            if s.status != "A":
                raise SlotConflictError()

        for i, slot in enumerate(slots):
            slot.status = "P"
            slot.registration_group = group
            slot.course_setup_hole = hole
            if i == 0:
                slot.member = member
            slot.save()

        self.logger.info("saved slots for member {} and group {}".format(member.id, group.id))

        return group


class NonLeagueEvent:

    def __init__(self, event):
        self.event = event

    def reserve(self, registrar, member, slot_ids=None, course_setup_hole_id=None, starting_order=0):

        if self.event.registration_maximum != 0:
            registrations = RegistrationSlot.objects.filter(event=self.event).count()
            if registrations >= self.event.registration_maximum:
                raise EventFullError()

        group = RegistrationGroup(event=self.event, course_setup=None, signed_up_by=registrar,
                                  starting_hole=1, starting_order=starting_order)
        group.expires = timezone.now() + timedelta(minutes=10)
        group.save()

        for s in range(0, self.event.maximum_signup_group_size):
            slot = RegistrationSlot(event=self.event, starting_order=starting_order, slot=s)
            slot.status = "P"
            slot.registration_group = group
            if s == 0:
                slot.member = member
            slot.save()

        return group


# class IndividualEvent:
#
#     def __init__(self, event):
#         self.event = event
#
#     def reserve(self, registrar, member, slot_ids=None, course_setup_hole_id=None, starting_order=0):
#
#         if self.event.registration_maximum != 0:
#             registrations = RegistrationSlot.objects.filter(event=self.event).count()
#             if registrations >= self.event.registration_maximum:
#                 raise EventFullError()
#
#         group = RegistrationGroup(event=self.event, course_setup=None, signed_up_by=registrar,
#                                   starting_hole=1, starting_order=starting_order)
#         group.expires = timezone.now() + timedelta(minutes=10)
#         group.save()
#
#         slot = RegistrationSlot(event=self.event, starting_order=starting_order, slot=0)
#         slot.status = "P"
#         slot.registration_group = group
#         slot.member = member
#         slot.save()
#
#         return group
