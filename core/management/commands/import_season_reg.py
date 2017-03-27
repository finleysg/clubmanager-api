import csv
import decimal

from django.core.management.base import BaseCommand
from datetime import datetime

# ghin,last_name,first_name,date_reserved,conf_number,event_fee,patron_card,gold_tees
from core.models import Member
from register.models import RegistrationGroup, RegistrationSlot
from events.models import Event


class Command(BaseCommand):
    help = 'Import new members from the given file'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        filename = options['file']
        count = 0
        dups = 0
        event = Event.objects.get(pk=46)  # TODO: use settings

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                ghin = row[0]
                last_name = row[1]
                first_name = row[2]
                date_reserved = row[3]
                dt_reserved = datetime.strptime(date_reserved, "%m/%d/%Y %H:%M")  # 2/24/2017 9:05
                conf_code = row[4]
                event_fee = decimal.Decimal(row[5].replace("$", ""))
                patron_card = decimal.Decimal(row[6].replace("$", ""))
                # (subtotal + this.transactionFixedCost) / (1.0 - this.transactionPercentage)
                subtotal = event_fee + patron_card
                payment_amt = (subtotal + decimal.Decimal("0.30")) / (1.0 - decimal.Decimal("0.029"))

                member = Member.objects.get(ghin=ghin)
                try:
                    RegistrationSlot.objects.get(event=event, member=member)
                    dups += 1
                except:
                    try:
                        group = RegistrationGroup(event=event, signed_up_by=member, payment_confirmation_code=conf_code,
                                                  payment_confirmation_timestamp=dt_reserved, payment_amount=payment_amt,
                                                  notes="Imported from existing system - online registration")
                        group.save()
                        print("group_id = {}, patron_flag = {}".format(group.id, (patron_card > 0)))
                        slot = RegistrationSlot(event=event, registration_group=group, member=member, status="R",
                                                is_event_fee_paid=True, is_greens_fee_paid=(patron_card > 0))
                        slot.save()
                    except Exception as e:
                        print(e)
                        print("error for {} {}".format(first_name, last_name))

                count += 1

        self.stdout.write(self.style.SUCCESS('Successfully imported %s registrations with %s skipped (already imported)' % (count, dups)))
