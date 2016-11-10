from django.db import models
from simple_history.models import HistoricalRecords
from events.models import Event

DOCUMENT_TYPE_CHOICES = (
    ("R", "Event Results"),
    ("S", "Season Long Points"),
    ("S", "Dam Cup"),
    ("M", "Match Play"),
    ("F", "Dinancial Statements")
)


class Document(models.Model):
    document_type = models.CharField(verbose_name="Type", choices=DOCUMENT_TYPE_CHOICES, max_length=1, default="R")
    title = models.CharField(verbose_name="Title", max_length=120)
    file = models.FileField(verbose_name="File", upload_to="documents/%Y")
    last_update = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(verbose_name="Event", to=Event, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.title
