import stripe
from django.db import models
from core.models import Member
from events.models import Event
from payments.managers import ChargeManager


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
