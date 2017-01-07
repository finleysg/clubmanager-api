from django.core.management.base import NoArgsCommand
from register.views import cancel_expired_slots


class Command(NoArgsCommand):
    help = 'Find and clear pending registrations that have expired'

    def handle_noargs(self, **options):
        count = cancel_expired_slots()
        self.stdout.write(self.style.SUCCESS('Cleared %s expired slots' % count))
