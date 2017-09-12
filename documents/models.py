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

PHOTO_TYPE_CHOICES = (
    ("DCT", "Dam Cup Team"),
    ("DCP", "Dam Cup Photos"),
    ("CC", "Club Champion"),
    ("SCC", "Senior Club Champion"),
    ("MW", "Major Winner"),
    ("EP", "Event Photos"),
    ("O", "Other")
)

SPONSOR_LEVEL = (
    ("G", "Gold"),
    ("S", "Silver"),
    ("B", "Bronze"),
    ("O", "Other"),
)


def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "documents/{0}/{1}".format(instance.year, filename)


def photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "photos/{0}/{1}".format(instance.year, filename)


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


class Photo(models.Model):
    photo_type = models.CharField(verbose_name="Type", choices=PHOTO_TYPE_CHOICES, max_length=3, default="EP")
    year = models.IntegerField(verbose_name="Golf Season", default=0)
    title = models.CharField(verbose_name="Title", max_length=120)
    file = models.ImageField(verbose_name="Image", upload_to=photo_directory_path)
    last_update = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(verbose_name="Event", to=Event, related_name="pictures", blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Sponsor(models.Model):
    name = models.CharField(verbose_name="Name", max_length=40, unique=True)
    description = models.TextField(verbose_name="Description", blank=True)
    website = models.CharField(verbose_name="Website URL", max_length=240)
    level = models.CharField(verbose_name="Level", choices=SPONSOR_LEVEL, max_length=1)
    ad_image = models.ImageField(verbose_name="Ad Image", upload_to="sponsor_images", blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
