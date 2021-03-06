from django.utils import timezone
# from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Max
from courses.models import CourseSetupHole


class RegistrationGroupManager(models.Manager):

    def clean_up_expired(self):
        groups = self.filter(expires__lt=timezone.now()).filter(payment_confirmation_code="")
        count = len(groups)

        for group in groups:
            # Make league slots available
            group.slots.filter(event__event_type="L") \
                .update(**{"status": "A", "registration_group": None, "member": None})

            # Delete non-league slots
            group.slots.exclude(event__event_type="L") \
                .delete()

            group.delete()

        return count


class RegistrationSlotManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('member', 'member__user')

    def is_registered(self, event_id, member_id):
        try:
            self.filter(event__id=event_id).filter(member__id=member_id).filter(status='R').get()
            return True
        except ObjectDoesNotExist:
            return False

    def members(self, event_id):
        return self.filter(event__id=event_id).values_list('member', flat=True)

    def remove_slots(self, event):
        self.filter(event=event).delete()

    def create_slots(self, event):
        slots = []

        if event.event_type == "L":
            for course_setup in event.course_setups.all():
                # for each hole in course setup, create an A and B group
                holes = CourseSetupHole.objects.filter(course_setup=course_setup)
                for hole in holes:
                    for s in range(0, event.group_size):
                        slot = self.create(event=event, course_setup_hole=hole, starting_order=0, slot=s)
                        slots.append(slot)
                    # Only add 2nd group on par 4s and 5s
                    if hole.hole.par != 3:
                        for s in range(0, event.group_size):
                            slot = self.create(event=event, course_setup_hole=hole, starting_order=1, slot=s)
                            slots.append(slot)

        return slots

    def remove_hole(self, event, hole, starting_order):
        self.filter(event=event, course_setup_hole=hole, starting_order=starting_order).delete()

    def add_slots(self, event, hole):
        slots = []
        start = 0

        # get max starting order and increment 1
        previous = self.filter(event=event, course_setup_hole=hole).aggregate(Max("starting_order"))
        if len(previous):
            start = previous["starting_order__max"] + 1

        for s in range(0, event.maximum_signup_group_size):
            slot = self.create(event=event, course_setup_hole=hole, starting_order=start, slot=s)
            slots.append(slot)

        return slots
