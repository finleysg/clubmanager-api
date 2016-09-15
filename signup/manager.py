from django.db import models
from courses.models import CourseSetupHole


class SignupSlotManager(models.Manager):
    def clear_slots(self, event):
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
        else:
            registrations = event.registration_maximum / event.maximum_signup_group_size
            if registrations == 0:
                registrations = 120 * event.maximum_signup_group_size
            for r in range(0, int(registrations)):
                for s in range(0, event.maximum_signup_group_size):
                    slot = self.create(event=event, starting_order=r, slot=s)
                    slots.append(slot)

        return slots

    def add_slots(self, event, hole):
        slots = []
        # TODO: get max starting order and increment 1
        for s in range(0, event.maximum_signup_group_size):
            slot = self.create(event=event, course_setup_hole=hole, starting_order=0, slot=s)
            slots.append(slot)
        return slots
