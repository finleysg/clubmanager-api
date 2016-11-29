from django.db import models
from simple_history.models import HistoricalRecords

from events.models import Event
from courses.models import CourseSetup, CourseSetupHole
from core.models import Member
from .manager import RegistrationSlotManager

STATUS_CHOICES = (
    ("A", "Available"),
    ("P", "Pending"),
    ("R", "Reserved"),
    ("U", "Unavailable")
)


class RegistrationGroup(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event)
    course_setup = models.ForeignKey(verbose_name="Course", to=CourseSetup, null=True)
    signed_up_by = models.ForeignKey(verbose_name="Signed up by", to=Member)
    starting_hole = models.IntegerField(verbose_name="Starting hole", blank=True)
    starting_order = models.IntegerField(verbose_name="Starting order", default=0)
    notes = models.TextField(verbose_name="Registration notes", blank=True)
    payment_confirmation_code = models.CharField(verbose_name="Payment confirmation code", max_length=120, blank=True)
    payment_confirmation_timestamp = models.DateTimeField(verbose_name="Payment confirmation timestamp", blank=True, null=True)
    payment_amount = models.DecimalField(verbose_name="Payment amount", max_digits=5, decimal_places=2, blank=True, null=True)

    history = HistoricalRecords()


class RegistrationSlot(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, related_name="registrations")
    course_setup_hole = models.ForeignKey(verbose_name="Hole", to=CourseSetupHole, null=True)
    registration_group = models.ForeignKey(verbose_name="Group", to=RegistrationGroup, blank=True, null=True, on_delete=models.SET_NULL, related_name="slots")
    member = models.ForeignKey(verbose_name="Member", to=Member, null=True)
    starting_order = models.IntegerField(verbose_name="Starting order", default=0)
    slot = models.IntegerField(verbose_name="Slot number", )
    status = models.CharField(verbose_name="Status", choices=STATUS_CHOICES, max_length=1, default="A")
    expires = models.DateTimeField(verbose_name="Expiration", null=True, blank=True)
    is_event_fee_paid = models.BooleanField(verbose_name="Event fee is paid", default=False)
    is_greens_fee_paid = models.BooleanField(verbose_name="Greens fee is paid", default=False)
    is_gross_skins_paid = models.BooleanField(verbose_name="Gross skins are paid", default=False)
    is_net_skins_paid = models.BooleanField(verbose_name="Net skins are paid", default=False)

    objects = RegistrationSlotManager()
    history = HistoricalRecords()
