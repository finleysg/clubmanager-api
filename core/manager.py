from django.db import models


class SettingsManager(models.Manager):

    def current_settings(self):
        return self.latest('year')


class MemberManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('user')
