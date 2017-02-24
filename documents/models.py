from django.db import models
from simple_history.models import HistoricalRecords
from events.models import Event

DOCUMENT_TYPE_CHOICES = (
    ("R", "Event Results"),
    ("T", "Event Tee Times"),
    ("P", "Season Long Points"),
    ("D", "Dam Cup"),
    ("M", "Match Play"),
    ("F", "Financial Statements"),
    ("S", "Sign Up"),
    ("O", "Other")
)


def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "documents/{0}/{1}".format(instance.year, filename)


class Document(models.Model):
    document_type = models.CharField(verbose_name="Type", choices=DOCUMENT_TYPE_CHOICES, max_length=1, default="R")
    year = models.IntegerField(verbose_name="Golf Season", default=0)
    title = models.CharField(verbose_name="Title", max_length=120)
    file = models.FileField(verbose_name="File", upload_to=document_directory_path)
    last_update = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(verbose_name="Event", to=Event, related_name="documents", blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.title
