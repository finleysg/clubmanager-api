import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Update members to active from file'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        filename = options['file']
        count = 0

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                ghin = int(row[3])

                try:
                    user = User.objects.get(ghin=ghin)
                    user.is_active = True
                    user.save()
                except Exception as e:
                    print(e)

                count += 1

        self.stdout.write(self.style.SUCCESS('Successfully updated %s members to active' % (count,)))
