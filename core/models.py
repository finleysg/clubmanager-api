from django.db import models
from imagekit.models import ImageSpecField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit


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
    show_email = models.BooleanField(verbose_name="Allow members to see my email address", default=True)
    show_phone = models.BooleanField(verbose_name="Allow members to see my phone number", default=True)
    raw_image = models.ImageField(verbose_name="Profile picture", upload_to="member_images", blank=True, null=True)
    thumbnail_image = ImageSpecField(source="raw_image", id="member:image:thumbnail_image")
    profile_image = ImageSpecField(source="raw_image", id="member:image:profile_image")

    history = HistoricalRecords()

    def formatted_phone_number(self):
        phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.phone_number)
        return phone

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)