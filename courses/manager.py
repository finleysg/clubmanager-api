from django.db import models

WEST = 1
NORTH = 4
EAST = 8


class CourseSetupManager(models.Manager):

    def append_default_courses(self, event):

        setups = []
        existing = event.course_setups.all()
        if event.event_type == "L" and len(existing) == 0:
            setups.append(self.filter(id=WEST).get())
            setups.append(self.filter(id=NORTH).get())
            setups.append(self.filter(id=EAST).get())
            event.course_setups = setups
