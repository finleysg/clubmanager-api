from django.db import models
from simple_history.models import HistoricalRecords


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    history = HistoricalRecords()

    def __str__(self):
        return self.name + ": " + self.description


class Hole(models.Model):
    course = models.ForeignKey(Course)
    default_hole_number = models.IntegerField(default=0)
    tee_name = models.CharField(max_length=12)
    par = models.IntegerField(default=0)
    default_handicap = models.IntegerField(blank=True, null=True)
    yardage = models.IntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return "Hole {} ({})".format(self.default_hole_number, self.tee_name)


class CourseSetup(models.Model):
    name = models.CharField(max_length=200)
    holes = models.IntegerField(default=18)
    slope = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    is_standard = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class CourseSetupHole(models.Model):
    course_setup = models.ForeignKey(CourseSetup)
    hole = models.ForeignKey(Hole)
    hole_number = models.IntegerField(default=0)
    handicap = models.IntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return "{}, hole {}".format(self.course_setup.name, self.hole_number)
