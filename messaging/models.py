from django.db import models
from simple_history.models import HistoricalRecords
from events.models import Event
from documents.models import Document


EVENT_LINK_CHOICES = (
    ("D", "Detail Page"),
    ("T", "Tee Time Page"),
    ("R", "Results Page")
)


class Announcement(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, blank=True, null=True)
    document = models.ForeignKey(verbose_name="Document", to=Document, blank=True, null=True)
    event_link_type = models.CharField(verbose_name="Link to", choices=EVENT_LINK_CHOICES, max_length=1, default="R", blank=True)
    external_url = models.CharField(verbose_name="External url", max_length=255, blank=True)
    external_name = models.CharField(verbose_name="External url name", max_length=40, blank=True)
    text = models.TextField(verbose_name="Announcement text")
    starts = models.DateTimeField(verbose_name="Display start")
    expires = models.DateTimeField(verbose_name="Display expiration")

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
