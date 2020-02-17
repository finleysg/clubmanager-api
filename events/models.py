from django.db import models
from django.db.models import DO_NOTHING
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
    ("D", "Deadline"),
    ("X", "Canceled"),
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
    notes = models.TextField(verbose_name="Additional notes", blank=True)
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    holes_per_round = models.IntegerField(verbose_name="Holes per round", default=18)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2, default=0.00)
    alt_event_fee = models.DecimalField(verbose_name="Alternative event fee", max_digits=5, decimal_places=2, default=0.00)
    skins_fee = models.DecimalField(verbose_name="Skins fee", max_digits=5, decimal_places=2, default=0.00)
    skins_type = models.CharField(verbose_name="Skins type", max_length=1, choices=SKIN_TYPE_CHOICES, default="N")
    green_fee = models.DecimalField(verbose_name="Green fee", max_digits=5, decimal_places=2, default=0.00)
    cart_fee = models.DecimalField(verbose_name="Cart fee", max_digits=5, decimal_places=2, default=0.00)
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

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )


class Event(models.Model):
    # From the template
    template = models.ForeignKey(to=EventTemplate, on_delete=DO_NOTHING)
    event_type = models.CharField(verbose_name="Event type", choices=EVENT_TYPE_CHOICES, max_length=1, default="L")
    name = models.CharField(verbose_name="Event title", max_length=100)
    description = models.TextField(verbose_name="Format and rules")
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    holes_per_round = models.IntegerField(verbose_name="Holes per round", default=18)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2, default=0.00)
    alt_event_fee = models.DecimalField(verbose_name="Alternative event fee", max_digits=5, decimal_places=2, default=0.00)
    skins_fee = models.DecimalField(verbose_name="Skins fee", max_digits=5, decimal_places=2, blank=0.00)
    skins_type = models.CharField(verbose_name="Skins type", max_length=1, choices=SKIN_TYPE_CHOICES, default="N")
    green_fee = models.DecimalField(verbose_name="Green fee", max_digits=5, decimal_places=2, default=0.00)
    cart_fee = models.DecimalField(verbose_name="Cart fee", max_digits=5, decimal_places=2, default=0.00)
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
    notes = models.TextField(verbose_name="Additional notes", blank=True, null=True)
    start_date = models.DateField(verbose_name="Start date")
    start_time = models.CharField(verbose_name="Starting time", max_length=40)
    signup_start = models.DateTimeField(verbose_name="Signup start", blank=True, null=True)
    signup_end = models.DateTimeField(verbose_name="Signup end", blank=True, null=True)
    skins_end = models.DateTimeField(verbose_name="Online skins deadline", blank=True, null=True)
    registration_maximum = models.IntegerField(verbose_name="Registration max (non-league events)", default=0)
    portal_url = models.CharField(verbose_name="Golf Genius Portal", max_length=240, blank=True, null=True)
    course_setups = models.ManyToManyField(verbose_name="Course(s)", to=CourseSetup, blank=True)

    history = HistoricalRecords()

    @property
    def enable_payments(self):
        return self.requires_registration and (self.event_fee > 0 or self.alt_event_fee > 0)

    def registration_window(self):
        state = "n/a"
        if self.requires_registration:
            state = "past"
            right_now = timezone.now()
            aware_start = pytz.utc.localize(datetime.combine(self.start_date, time=datetime.min.time()))
            signup_start = pytz.utc.normalize(self.signup_start)
            signup_end = pytz.utc.normalize(self.signup_end)

            if signup_start < right_now and signup_end > right_now:
                state = "registration"
            elif signup_start > right_now:
                state = "future"
            elif state == "past" and aware_start > right_now:
                state = "pending"

        return state

    def validate_signup_window(self):
        if self.requires_registration:
            if self.signup_start is None or self.signup_end is None:
                raise ValueError('When an event requires registration, both signup start and signup end are required')
            if self.signup_start > self.signup_end:
                raise ValueError('The signup start must be earlier than signup end')

    def __str__(self):
        return "{} {}".format(self.start_date, self.name)

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )
