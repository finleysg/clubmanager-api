from django.db import models
from simple_history.models import HistoricalRecords

from courses.models import CourseSetup

EVENT_TYPE_CHOICES = (
    ("L", "League"),
    ("M", "Weekend Major"),
    ("H", "Holiday Pro-shop Event"),
    ("O", "Other"),
)
SCORING_CHOICES = (
    ("IN", "Individual"),
    ("TBB", "Team: Best Ball"),
    ("TAG", "Team: Aggregate Score"),
    ("TS", "Team: Scramble"),
    ("TA", "Team: Alternate Shot"),
    ("TC", "Team: Combination"),
)
SCORING_SYSTEM_CHOICES = (
    ("SP", "Stroke Play"),
    ("SF", "Stableford"),
    ("CH", "Chicago"),
)
START_TYPE_CHOICES = (
    ("TT", "Tee Times"),
    ("FB", "Front and Back"),
    ("SG", "Shotgun"),
)
SKIN_TYPE_CHOICES = (
    ("I", "Individual"),
    ("T", "Team"),
    ("N", "No Skins"),
)

class EventTemplate(models.Model):
    event_type = models.CharField(verbose_name="Event type", choices=EVENT_TYPE_CHOICES, max_length=1, default="M")
    name = models.CharField(verbose_name="Event title", max_length=100)
    description = models.TextField(verbose_name="Format and rules")
    notes = models.TextField(verbose_name="Additional notes")
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    holes_per_round = models.IntegerField(verbose_name="Holes per round", default=18)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2)
    skins_fee = models.DecimalField(verbose_name="Skins fee", max_digits=5, decimal_places=2, default=0.00)
    skins_type = models.CharField(verbose_name="Skins type", max_length=1, choices=SKIN_TYPE_CHOICES, default="N")
    minimum_signup_group_size = models.IntegerField(verbose_name="Minimum sign-up group size", default=1)
    maximum_signup_group_size = models.IntegerField(verbose_name="Maximum sign-up group size", default=1)
    group_size = models.IntegerField(verbose_name="Group size", default=4)
    start_type = models.CharField(verbose_name="Start type", choices=START_TYPE_CHOICES, max_length=2, default="TT")
    can_signup_group = models.BooleanField(verbose_name="Member can sign up group", default=False)
    can_choose_hole = models.BooleanField(verbose_name="Member can choose starting hole", default=False)
    scoring = models.CharField(verbose_name="Scoring type", choices=SCORING_CHOICES, max_length=3, default="IN")
    scoring_system = models.CharField(verbose_name="Scoring system", choices=SCORING_SYSTEM_CHOICES, max_length=2, default="SP")
    number_of_scores = models.CharField(verbose_name="Number of scores", max_length=12, default="1", blank=True)
    season_points = models.IntegerField(verbose_name="Season long points available", default=0)

    history = HistoricalRecords()

    def __str__(self):
        return "({}) {}".format(self.event_type, self.name)


class Event(models.Model):
    # From the template
    template = models.ForeignKey(to=EventTemplate)
    event_type = models.CharField(verbose_name="Event type", choices=EVENT_TYPE_CHOICES, max_length=1, default="M")
    name = models.CharField(verbose_name="Event title", max_length=100)
    description = models.TextField(verbose_name="Format and rules")
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    holes_per_round = models.IntegerField(verbose_name="Holes per round", default=18)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2)
    skins_fee = models.DecimalField(verbose_name="Skins fee", max_digits=5, decimal_places=2, blank=True)
    skins_type = models.CharField(verbose_name="Skins type", max_length=1, choices=SKIN_TYPE_CHOICES, default="N")
    minimum_signup_group_size = models.IntegerField(verbose_name="Minimum sign-up group size", default=1)
    maximum_signup_group_size = models.IntegerField(verbose_name="Maximum sign-up group size", default=1)
    group_size = models.IntegerField(verbose_name="Group size", default=4)
    start_type = models.CharField(verbose_name="Start type", choices=START_TYPE_CHOICES, max_length=2, default="TT")
    can_signup_group = models.BooleanField(verbose_name="Member can sign up group", default=False)
    can_choose_hole = models.BooleanField(verbose_name="Member can choose starting hole", default=False)
    scoring = models.CharField(verbose_name="Scoring type", choices=SCORING_CHOICES, max_length=3, default="IN")
    scoring_system = models.CharField(verbose_name="Scoring system", choices=SCORING_SYSTEM_CHOICES, max_length=2, default="SP")
    number_of_scores = models.CharField(verbose_name="Number of scores", max_length=12, default="1", blank=True)
    season_points = models.IntegerField(verbose_name="Season long points available", default=0)
    # Event instance specific
    notes = models.TextField(verbose_name="Additional notes")
    start_date = models.DateField(verbose_name="Start date")
    end_date = models.DateField(verbose_name="End date (multi-day events)", blank=True, null=True)
    signup_start = models.DateTimeField(verbose_name="Signup start")
    signup_end = models.DateTimeField(verbose_name="Signup end")
    start_time = models.TimeField(verbose_name="Starting time")
    end_time = models.TimeField(verbose_name="Ending time (non-shotgun starts)", blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
