import csv
import decimal

from django.core.management.base import BaseCommand
from datetime import datetime

# 0-ghin,1-last_name,2-first_name,3-signup_member_ghin,4-date_reserved,5-conf_number,6-legacy_id,7-event_fee,8-gross_skins,9-net_skins,10-green_fee,11-cart_fee
from core.models import Member
from register.models import RegistrationGroup, RegistrationSlot
from events.models import Event


# TODO: need to determine the right hole and starting position
class Command(BaseCommand):
    help = 'Import event signups from the given file'

    def add_arguments(self, parser):
        parser.add_argument('event')
        parser.add_argument('file')

    def handle(self, *args, **options):
        filename = options['file']
        count = 0
        dups = 0
        event_id = int(options['event'])
        event = Event.objects.get(pk=event_id)

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                try:
                    ghin = row[0]
                    last_name = row[1]
                    first_name = row[2]
                    sign_up_member_ghin = row[3]
                    date_reserved = row[4]
                    dt_reserved = datetime.strptime(date_reserved, "%m/%d/%Y %H:%M")  # 2/24/2017 9:05
                    conf_code = row[5]
                    legacy_event_id = row[6]
                    event_fee = decimal.Decimal(row[7].replace("$", ""))
                    gross_skins = decimal.Decimal(row[8].replace("$", ""))
                    net_skins = decimal.Decimal(row[9].replace("$", ""))
                    green_fee = decimal.Decimal(row[10].replace("$", ""))
                    cart_fee = decimal.Decimal(row[11].replace("$", ""))

                    member = Member.objects.get(ghin=ghin)
                    signup_member = Member.objects.get(ghin=sign_up_member_ghin)
                    try:
                        RegistrationSlot.objects.get(event=event, member=member)
                        dups += 1
                    except:
                        try:
                            group = RegistrationGroup.objects.get(event=event, signed_up_by=signup_member)
                        except:
                            group = RegistrationGroup(event=event, signed_up_by=signup_member, payment_confirmation_code=conf_code,
                                                      payment_confirmation_timestamp=dt_reserved, payment_amount=0.00,
                                                      notes="Imported from existing system - legacy event id " + legacy_event_id)
                            group.save()

                        slot = RegistrationSlot(event=event, registration_group=group, member=member, status="R",
                                                is_event_fee_paid=(event_fee > 0),
                                                is_gross_skins_paid=(gross_skins > 0),
                                                is_net_skins_paid=(net_skins > 0),
                                                is_cart_fee_paid=(cart_fee > 0),
                                                is_greens_fee_paid=(green_fee > 0))
                        slot.save()

                    count += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR("Failed to import {} {}:".format(first_name, last_name)))
                    self.stderr.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS('Successfully imported %s registrations with %s skipped (already imported)' % (count, dups)))
