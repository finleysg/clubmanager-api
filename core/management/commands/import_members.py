import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import datetime

# Last_Name,First_Name,DOB,MemNumber,HOMEPHONE,BUSPhone,Joined,EMAIL,ShowPhone,SecLevel,hdcp,Home_hdcp,Occupation,adminflag
from core.models import Member


class Command(BaseCommand):
    help = 'Import new members from the given file'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        filename = options['file']
        count = 0
        dups = 0

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                last_name = row[0]
                first_name = row[1]
                birth_date = row[2]
                bd = None
                if birth_date != "":
                    birth_date = birth_date.replace(" 00:00:00", "")
                    if birth_date != "0000-00-00":
                        bd = datetime.strptime(birth_date, '%Y-%m-%d')
                ghin = int(row[3])
                year = row[6]
                year = int(year) if year is not None else 1900
                year = 1900 if year == 0 else year
                username = "%s%s" % (first_name.lower(), last_name.lower())
                email = row[7]
                email = email.lower() if email is not None else "%s@nunya.com" % username
                email = "%s@nunya.com" % username if email == "" else email

                date_joined = datetime(year=year, month=3, day=31)

                try:
                    user = User.objects.create_user(last_name=last_name, first_name=first_name, email=email, username=username, date_joined=date_joined, password=str(ghin))
                    member = Member(user=user, ghin=str(ghin), birth_date=bd)
                    member.save()
                    print(user.email)
                except:
                    print("error: " + username)
                    dups += 1

                count += 1

        self.stdout.write(self.style.SUCCESS('Successfully imported %s members with %s skipped to due error' % (count, dups)))