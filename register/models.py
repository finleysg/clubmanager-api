import stripe

from django.db import models
from simple_history.models import HistoricalRecords

from events.models import Event
from courses.models import CourseSetup, CourseSetupHole
from core.models import Member
from .manager import SignupSlotManager, ChargeManager

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


class SignupSlot(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event)
    course_setup_hole = models.ForeignKey(verbose_name="Hole", to=CourseSetupHole, null=True)
    registration_group = models.ForeignKey(verbose_name="Group", to=RegistrationGroup, blank=True, null=True, on_delete=models.SET_NULL, related_name="slots")
    member = models.ForeignKey(verbose_name="Member", to=Member, null=True)
    starting_order = models.IntegerField(verbose_name="Starting order", default=0)
    slot = models.IntegerField(verbose_name="Slot number", )
    status = models.CharField(verbose_name="Status", choices=STATUS_CHOICES, max_length=1, default="A")
    expires = models.DateTimeField(verbose_name="Expiration", null=True, blank=True)

    objects = SignupSlotManager()
    history = HistoricalRecords()


class Registration(models.Model):
    registration_group = models.ForeignKey(verbose_name="Group", to=RegistrationGroup)
    member = models.ForeignKey(verbose_name="Member", to=Member)
    is_event_fee_paid = models.BooleanField(verbose_name="Event fee is paid", default=False)
    is_greens_fee_paid = models.BooleanField(verbose_name="Greens fee is paid", default=False)
    is_gross_skins_paid = models.BooleanField(verbose_name="Gross skins are paid", default=False)
    is_net_skins_paid = models.BooleanField(verbose_name="Net skins are paid", default=False)

    history = HistoricalRecords()


class Charge(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True)
    member = models.ForeignKey(Member, related_name="charges")
    event = models.ForeignKey(Event, related_name="charges")
    source = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default="usd")
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    amount_refunded = models.DecimalField(
        decimal_places=2,
        max_digits=9,
        null=True
    )
    description = models.TextField(blank=True)
    paid = models.NullBooleanField(null=True)
    refunded = models.NullBooleanField(null=True)
    captured = models.NullBooleanField(null=True)
    receipt_sent = models.BooleanField(default=False)
    charge_created = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="unknown")

    objects = ChargeManager()

    @property
    def stripe_charge(self):
        return stripe.Charge.retrieve(self.stripe_id)
