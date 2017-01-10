from django.db import models
from simple_history.models import HistoricalRecords
from events.models import Event
from documents.models import Document


class Announcement(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, blank=True, null=True)
    document = models.ForeignKey(verbose_name="Document", to=Document, blank=True, null=True)
    external_url = models.CharField(verbose_name="External url", max_length=255, blank=True)
    external_name = models.CharField(verbose_name="External url name", max_length=40, blank=True)
    title = models.CharField(verbose_name="Title", max_length=100, blank=True)
    text = models.TextField(verbose_name="Announcement text")
    starts = models.DateTimeField(verbose_name="Display start")
    expires = models.DateTimeField(verbose_name="Display expiration")
    members_only = models.BooleanField(verbose_name="For members only?", default=True)

    history = HistoricalRecords()

    @property
    def short_text(self):
        return "".join(self.text.split()[:20])

    def __str__(self):
        return self.short_text


class ContactMessage(models.Model):
    full_name = models.CharField(verbose_name="Full name", max_length=100)
    email = models.CharField(verbose_name="Email", max_length=254)
    message_text = models.TextField(verbose_name="Message text")
    message_date = models.DateTimeField(verbose_name="Message date", auto_now_add=True)
