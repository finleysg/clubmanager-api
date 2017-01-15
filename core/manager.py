from django.db import models


class SettingsManager(models.Manager):

    def current_settings(self):
        return self.latest('year')


# class MemberManager(models.Manager):
#
#     def current_members(self):
#         ss = SeasonSettings.objects.current_settings()
#         self.select_related()
