from django.db import models
from simple_history.models import HistoricalRecords

from courses.models import CourseSetup

SCORING_CHOICES = (
    ("IN", "Individual"),
    ("T1", "Team: One Score"),
    ("TM", "Team: Multiple Scores")
)
SCORING_SYSTEM_CHOICES = (
    ("SP", "Stroke Play"),
    ("SF", "Stableford"),
    ("CH", "Chicago")
)
TEAM_SCORING_CHOICES = (
    ("NA", "Not a Team Event"),
    ("BB", "Best Ball"),
    ("AGG", "Aggregate")
)


class EventTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    rounds = models.IntegerField(default=1)
    holes = models.IntegerField(default=18)
    event_fee = models.DecimalField(max_digits=5, decimal_places=2)
    skins_fee = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_signup_group_size = models.IntegerField(default=1)
    maximum_signup_group_size = models.IntegerField(default=1)
    group_size = models.IntegerField(default=4)
    is_shotgun_start = models.BooleanField(default=False)
    can_signup_group = models.BooleanField(default=False)
    can_choose_hole = models.BooleanField(default=False)
    scoring = models.CharField(choices=SCORING_CHOICES, max_length=2, default="IN")
    scoring_system = models.CharField(choices=SCORING_SYSTEM_CHOICES, max_length=2, default="SP")
    team_scoring = models.CharField(choices=TEAM_SCORING_CHOICES, max_length=2, default="NA")
    number_of_scores = models.IntegerField(default=1)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(CourseSetup)
    description = models.TextField()
    start_date = models.DateField()
    rounds = models.IntegerField(default=1)
    holes = models.IntegerField(default=18)
    signup_start = models.DateTimeField()
    signup_end = models.DateTimeField()
    start_time = models.TimeField()
    event_fee = models.DecimalField(max_digits=5, decimal_places=2)
    skins_fee = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_signup_group_size = models.IntegerField(default=1)
    maximum_signup_group_size = models.IntegerField(default=1)
    group_size = models.IntegerField(default=4)
    is_shotgun_start = models.BooleanField(default=False)
    can_signup_group = models.BooleanField(default=False)
    can_choose_hole = models.BooleanField(default=False)
    scoring = models.CharField(choices=SCORING_CHOICES, max_length=2, default="IN")
    scoring_system = models.CharField(choices=SCORING_SYSTEM_CHOICES, max_length=2, default="SP")
    team_scoring = models.CharField(choices=TEAM_SCORING_CHOICES, max_length=2, default="NA")
    number_of_scores = models.IntegerField(default=1)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
