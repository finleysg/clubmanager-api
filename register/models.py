from django.db import models
from simple_history.models import HistoricalRecords

from events.models import Event
from courses.models import CourseSetup, CourseSetupHole
from core.models import Member
from .manager import RegistrationSlotManager, RegistrationGroupManager

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
    expires = models.DateTimeField(verbose_name="Expiration", null=True, blank=True)
    starting_hole = models.IntegerField(verbose_name="Starting hole", blank=True, default=1)
    starting_order = models.IntegerField(verbose_name="Starting order", default=0)
    notes = models.TextField(verbose_name="Registration notes", blank=True)
    card_verification_token = models.CharField(verbose_name="Card verification token", max_length=30, blank=True)
    payment_confirmation_code = models.CharField(verbose_name="Payment confirmation code", max_length=30, blank=True)
    payment_confirmation_timestamp = models.DateTimeField(verbose_name="Payment confirmation timestamp", blank=True, null=True)
    payment_amount = models.DecimalField(verbose_name="Payment amount", max_digits=5, decimal_places=2, blank=True, null=True)

    objects = RegistrationGroupManager()
    history = HistoricalRecords()

    @property
    def members(self):
        member_names = []
        for slot in self.slots.all():
            if slot.member is not None:
                member_names.append(slot.member.member_name())
        return ", ".join(member_names)

    def __str__(self):
        return "{} group: {}".format(self.event.name, self.signed_up_by)


class RegistrationSlot(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, related_name="registrations")
    course_setup_hole = models.ForeignKey(verbose_name="Hole", to=CourseSetupHole, null=True)
    registration_group = models.ForeignKey(verbose_name="Group", to=RegistrationGroup, blank=True, null=True, on_delete=models.SET_NULL, related_name="slots")
    member = models.ForeignKey(verbose_name="Member", to=Member, blank=True, null=True)
    starting_order = models.IntegerField(verbose_name="Starting order", default=0)
    slot = models.IntegerField(verbose_name="Slot number", default=0)
    status = models.CharField(verbose_name="Status", choices=STATUS_CHOICES, max_length=1, default="A")
    is_event_fee_paid = models.BooleanField(verbose_name="Event fee", default=False)
    is_greens_fee_paid = models.BooleanField(verbose_name="Greens fee", default=False)
    is_cart_fee_paid = models.BooleanField(verbose_name="Cart fee", default=False)
    is_gross_skins_paid = models.BooleanField(verbose_name="Gross skins", default=False)
    is_net_skins_paid = models.BooleanField(verbose_name="Net skins", default=False)

    objects = RegistrationSlotManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.status


class RegistrationSlotPayment(models.Model):
    registration_slot = models.ForeignKey(verbose_name="Registration", to=RegistrationSlot, related_name="payments")
    recorded_by = models.ForeignKey(verbose_name="Member", to=Member)
    card_verification_token = models.CharField(verbose_name="Card verification token", max_length=30, blank=True)
    payment_code = models.CharField(verbose_name="Payment code", max_length=30, blank=True)
    payment_timestamp = models.DateTimeField(verbose_name="Payment timestamp", auto_now=True)
    payment_amount = models.DecimalField(verbose_name="Payment amount", max_digits=5, decimal_places=2, blank=True, null=True)
    comment = models.CharField(verbose_name="Comment", max_length=200, blank=True)

    history = HistoricalRecords()


class RegistrationRefund(models.Model):
    related_record_id = models.IntegerField(verbose_name="Related record id")
    related_record_name = models.CharField(verbose_name="Related record name", max_length=30)
    recorded_by = models.ForeignKey(verbose_name="Recorded by", to=Member)
    refund_code = models.CharField(verbose_name="Refund code", max_length=30)
    refund_timestamp = models.DateTimeField(verbose_name="Refund timestamp", auto_now=True)
    refund_amount = models.DecimalField(verbose_name="Refund amount", max_digits=5, decimal_places=2)
    comment = models.CharField(verbose_name="Comment", max_length=200, blank=True)

    history = HistoricalRecords()


class OnlinePayment(models.Model):

    class Meta:
        verbose_name_plural = "Online Payments"
        db_table = "online_payment_view"
        managed = False

    event_id = models.IntegerField(verbose_name="Event Id")
    name = models.CharField(verbose_name="Event Name", max_length=100)
    event_type = models.CharField(verbose_name="Event Type", max_length=1)
    start_date = models.DateField(verbose_name="Start Date")
    signed_up_by_id = models.IntegerField(verbose_name="Member Id")
    first_name = models.CharField(verbose_name="Member First Name", max_length=40)
    last_name = models.CharField(verbose_name="Member Last Name", max_length=60)
    payment_confirmation_code = models.CharField(verbose_name="Payment Confirmation Code", max_length=30)
    payment_confirmation_timestamp = models.DateTimeField(verbose_name="Payment Confirmation Timestamp")
    payment_amount = models.DecimalField(verbose_name="Payment Amount", max_digits=5, decimal_places=2)
    record_id = models.IntegerField(verbose_name="Record Id")
    record_type = models.CharField(verbose_name="Record Type", max_length=12)
    refund_code = models.CharField(verbose_name="Refund Confirmation Code", max_length=12)
    refund_timestamp = models.DateTimeField(verbose_name="Refund Confirmation Timestamp")
    refund_amount = models.DecimalField(verbose_name="Refund Amount", max_digits=5, decimal_places=2)
    comment = models.CharField(verbose_name="Refund Comment", max_length=12)
    refunded_by = models.CharField(verbose_name="Refunded By", max_length=12)
    pkey = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return "{} ({}) on {} - {} {}".format(self.name, self.event_type, self.start_date, self.first_name, self.last_name)
