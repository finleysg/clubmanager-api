from django.db import models
from events.models import Event
from courses.models import CourseSetup, CourseSetupHole
from core.models import Member

STATUS_CHOICES = (
    ("A", "Available"),
    ("P", "Pending"),
    ("R", "Reserved"),
    ("U", "Unavailable")
)


class SignupReservation(models.Model):
    event = models.ForeignKey(Event)
    course_setup = models.ForeignKey(CourseSetup)
    starting_hole = models.IntegerField()
    starting_order = models.IntegerField(default=0)
    # start_time = models.TimeField(null=True)


class Signup(models.Model):
    signup_reservation = models.ForeignKey(SignupReservation)
    member = models.ForeignKey(Member)
    is_event_fee_paid = models.BooleanField(default=False)
    is_greens_fee_paid = models.BooleanField(default=False)
    is_gross_skins_paid = models.BooleanField(default=False)
    is_net_skins_paid = models.BooleanField(default=False)
    signed_up_by = models.CharField(max_length=60)
    payment_confirmation_code = models.CharField(max_length=120, null=True, blank=True)


class SignupSlot(models.Model):
    event = models.ForeignKey(Event)
    course_setup_hole_id = models.ForeignKey(CourseSetupHole)
    signup_reservation = models.ForeignKey(SignupReservation, null=True)
    member = models.ForeignKey(Member, null=True)
    starting_order = models.IntegerField(default=0)
    slot = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default="A")
    expires = models.DateTimeField(null=True)
