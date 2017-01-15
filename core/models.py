from django.db import models
from imagekit.models import ImageSpecField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit
from datetime import datetime

from core.manager import SettingsManager
from events.models import Event


class ThumbnailSpec(ImageSpec):
    format = "JPEG"
    options = {"quality": 75}
    processors = [ResizeToFit(64, 64)]


class ProfileSpec(ImageSpec):
    format = "JPEG"
    options = {"quality": 85}
    processors = [ResizeToFit(400, 400)]


class Club(models.Model):
    description = models.CharField(max_length=200)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    contact_email = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.description


class SeasonSettings(models.Model):
    year = models.IntegerField(verbose_name="Current golf season")
    reg_event = models.ForeignKey(verbose_name="Registration event", to=Event, related_name="registration")
    match_play_event = models.ForeignKey(verbose_name="Match play event", to=Event, related_name="match_play", blank=True, null=True)
    accept_new_members = models.BooleanField(verbose_name="Accepting new member registration?", default=False)

    objects = SettingsManager()


register.generator('member:image:thumbnail_image', ThumbnailSpec)
register.generator('member:image:profile_image', ProfileSpec)


class Member(models.Model):
    user = models.OneToOneField(User)
    address1 = models.CharField(verbose_name="Address", max_length=100, blank=True, null=True)
    address2 = models.CharField(verbose_name="Address line 2", max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True, null=True)
    state = models.CharField(verbose_name="State", max_length=20, blank=True, null=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True, null=True)
    phone_number = models.CharField(verbose_name="Phone number", max_length=20, blank=True, null=True)
    ghin = models.CharField(verbose_name="GHIN", max_length=7, blank=True, null=True)
    handicap = models.DecimalField(verbose_name="Handicap index", max_digits=3, decimal_places=1, blank=True, null=True)
    handicap_revision_date = models.DateField(verbose_name="Handicap revision date", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Birth date", blank=True, null=True)
    summary = models.TextField(verbose_name="Summary", blank=True, null=True)
    status = models.CharField(verbose_name="Status", max_length=140, blank=True, null=True)
    stripe_customer_id = models.CharField(verbose_name="Stripe ID", max_length=255, blank=True, null=True)
    raw_image = models.ImageField(verbose_name="Profile picture", upload_to="member_images", blank=True, null=True)
    thumbnail_image = ImageSpecField(source="raw_image", id="member:image:thumbnail_image")
    profile_image = ImageSpecField(source="raw_image", id="member:image:profile_image")
    favorites = models.ManyToManyField("self", blank=True)
    forward_tees = models.BooleanField(verbose_name="Forward tee player", default=False)

    history = HistoricalRecords()

    def member_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def member_email(self):
        return self.user.email

    def age(self):
        my_age = 0
        if self.birth_date:
            my_age = (datetime.utcnow() - self.birth_date).total_years()
        return my_age

    def thumbnail_url(self):
        if self.raw_image:
            return self.thumbnail_image.url
        return None

    def profile_url(self):
        if self.raw_image:
            return self.profile_image.url
        return None

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
