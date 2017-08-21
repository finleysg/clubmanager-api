from django.core.management.base import BaseCommand

from core.models import Member
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Set password to GHIN for all members'

    def handle(self, *args, **options):
        count = 0
        members = Member.objects.all()

        for member in members:
            try:
                if member.user.last_name != "Finley":
                    pw = member.ghin
                    member.user.set_password(pw)
                    member.user.save()
                    count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR("Failed to update {}:".format(member.member_name())))
                self.stderr.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS('Successfully updated {} members'.format(count)))
