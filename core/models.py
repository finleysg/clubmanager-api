from django.db import models
from imagekit.models import ImageSpecField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit
from datetime import datetime


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
    show_email = models.BooleanField(verbose_name="Allow members to see my email address", default=True)
    raw_image = models.ImageField(verbose_name="Profile picture", upload_to="member_images", blank=True, null=True)
    thumbnail_image = ImageSpecField(source="raw_image", id="member:image:thumbnail_image")
    profile_image = ImageSpecField(source="raw_image", id="member:image:profile_image")
    favorites = models.ManyToManyField("self", blank=True)

    history = HistoricalRecords()

    def member_email(self):
        email = "xxxxxxxxx@xxxxx.xxx"
        if self.show_email:
            email = self.user.email
        return email

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
