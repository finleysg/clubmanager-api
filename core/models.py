from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User


class Club(models.Model):
    description = models.CharField(max_length=200)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    contact_email = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.description


class Member(models.Model):
    user = models.OneToOneField(User)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    ghin = models.CharField(max_length=7, blank=True, null=True)
    handicap = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    handicap_revision_date = models.DateField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)