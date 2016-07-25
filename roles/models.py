from django.db import models
from simple_history.models import HistoricalRecords

from core.models import Member

ROLE_TYPE_CHOICES = (
    ("B", "Board"),
    ("M", "Committee"),
    ("C", "Captain"),
    ("G", "Golf Staff"),
)


class Role(models.Model):
    role_type = models.CharField(verbose_name="Type", choices=ROLE_TYPE_CHOICES, max_length=1, default="B")
    title = models.CharField(verbose_name="Title", max_length=120)
    description = models.TextField(verbose_name="Responsibilities", blank=True)
    members = models.ManyToManyField(Member, through='RoleMember')

    history = HistoricalRecords()

    def __str__(self):
        return self.title


class RoleMember(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    expires = models.IntegerField(verbose_name="Expires", blank=True)
    is_chair = models.BooleanField(verbose_name="Is Chair", default=False)
    is_officer = models.BooleanField(verbose_name="Is Officer", default=False)
