from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
from datetime import datetime
import pytz

from courses.models import CourseSetup

EVENT_TYPE_CHOICES = (
    ("L", "League"),
    ("W", "Weekend Major"),
    ("H", "Holiday Pro-shop Event"),
    ("M", "Member Meeting"),
    ("B", "Board Meeting"),
    ("O", "Other"),
    ("S", "State Tournament"),
    ("R", "Open Registration Period"),
)
START_TYPE_CHOICES = (
    ("TT", "Tee Times"),
    ("SG", "Shotgun"),
    ("NA", "Not Applicable"),
)
SKIN_TYPE_CHOICES = (
    ("I", "Individual"),
    ("T", "Team"),
    ("N", "No Skins"),
)


class EventTemplate(models.Model):
    event_type = models.CharField(verbose_name="Event type", choices=EVENT_TYPE_CHOICES, max_length=1, default="L")
    name = models.CharField(verbose_name="Event title", max_length=100)
    description = models.TextField(verbose_name="Format and rules")
    notes = models.TextField(verbose_name="Additional notes")
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    holes_per_round = models.IntegerField(verbose_name="Holes per round", default=18)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2, default=0.00)
    skins_fee = models.DecimalField(verbose_name="Skins fee", max_digits=5, decimal_places=2, default=0.00)
    skins_type = models.CharField(verbose_name="Skins type", max_length=1, choices=SKIN_TYPE_CHOICES, default="N")
    minimum_signup_group_size = models.IntegerField(verbose_name="Minimum sign-up group size", default=1)
    maximum_signup_group_size = models.IntegerField(verbose_name="Maximum sign-up group size", default=1)
    group_size = models.IntegerField(verbose_name="Group size", default=4)
    start_type = models.CharField(verbose_name="Start type", choices=START_TYPE_CHOICES, max_length=2, default="NA")
    can_signup_group = models.BooleanField(verbose_name="Member can sign up group", default=False)
    can_choose_hole = models.BooleanField(verbose_name="Member can choose starting hole", default=False)
    season_points = models.IntegerField(verbose_name="Season long points available", default=0)
    requires_registration = models.BooleanField(verbose_name="Requires registration", default=True)
    external_url = models.CharField(verbose_name="External url", max_length=255, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return "({}) {}".format(self.event_type, self.name)


class Event(models.Model):
    # From the template
    template = models.ForeignKey(to=EventTemplate)
    event_type = models.CharField(verbose_name="Event type", choices=EVENT_TYPE_CHOICES, max_length=1, default="L")
    name = models.CharField(verbose_name="Event title", max_length=100)
    description = models.TextField(verbose_name="Format and rules")
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    holes_per_round = models.IntegerField(verbose_name="Holes per round", default=18)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2, default=0.00)
    skins_fee = models.DecimalField(verbose_name="Skins fee", max_digits=5, decimal_places=2, blank=0.00)
    skins_type = models.CharField(verbose_name="Skins type", max_length=1, choices=SKIN_TYPE_CHOICES, default="N")
    minimum_signup_group_size = models.IntegerField(verbose_name="Minimum sign-up group size", default=1)
    maximum_signup_group_size = models.IntegerField(verbose_name="Maximum sign-up group size", default=1)
    group_size = models.IntegerField(verbose_name="Group size", default=4)
    start_type = models.CharField(verbose_name="Start type", choices=START_TYPE_CHOICES, max_length=2, default="NA")
    can_signup_group = models.BooleanField(verbose_name="Member can sign up group", default=False)
    can_choose_hole = models.BooleanField(verbose_name="Member can choose starting hole", default=False)
    season_points = models.IntegerField(verbose_name="Season long points available", default=0)
    requires_registration = models.BooleanField(verbose_name="Requires registration", default=True)
    external_url = models.CharField(verbose_name="External url", max_length=255, blank=True, null=True)
    # Event instance specific
    notes = models.TextField(verbose_name="Additional notes")
    start_date = models.DateField(verbose_name="Start date")
    start_time = models.CharField(verbose_name="Starting time", max_length=40)
    signup_start = models.DateTimeField(verbose_name="Signup start", blank=True, null=True)
    signup_end = models.DateTimeField(verbose_name="Signup end", blank=True, null=True)
    registration_maximum = models.IntegerField(verbose_name="Registration max (non-league events)", default=0)
    course_setups = models.ManyToManyField(verbose_name="Course(s)", to=CourseSetup, blank=True)

    history = HistoricalRecords()

    @property
    def enable_payments(self):
        return self.requires_registration and self.event_fee > 0

    def registration_window(self):
        right_now = timezone.now()
        aware_start = pytz.utc.localize(datetime.combine(self.start_date, time=datetime.min.time()))
        state = "n/a"

        if self.requires_registration:
            state = "past"
            if self.signup_start < right_now and self.signup_end > right_now:
                state = "registration"
            elif self.signup_start > right_now:
                state = "future"
            elif state == "past" and aware_start > right_now:
                state = "pending"

        return state

    def __str__(self):
        return self.name
