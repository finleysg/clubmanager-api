from django.core.management.base import BaseCommand
from register.registration_cache import load_cache


class Command(BaseCommand):
    help = 'Primes the registration cache for the given event id'

    def add_arguments(self, parser):
        parser.add_argument('event_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for event_id in options['event_id']:
            load_cache(event_id)

            self.stdout.write(self.style.SUCCESS('Successfully primed the cache for "%s"' % event_id))
