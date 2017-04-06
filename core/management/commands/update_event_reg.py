import decimal

from django.core.management.base import BaseCommand

from register.models import RegistrationGroup, RegistrationSlot
from events.models import Event


class Command(BaseCommand):
    help = 'Update payment amounts for imported event reg'

    def add_arguments(self, parser):
        parser.add_argument('event')

    def handle(self, *args, **options):
        count = 0
        event_id = int(options['event'])
        event = Event.objects.get(pk=event_id)
        groups = RegistrationGroup.objects.filter(event=event)

        for group in groups:
            try:
                subtotal = decimal.Decimal('0.0')

                registrations = RegistrationSlot.objects.filter(registration_group=group)
                for reg in registrations:
                    if reg.is_event_fee_paid:
                        subtotal += event.event_fee
                    if reg.is_gross_skins_paid:
                        subtotal += event.skins_fee
                    if reg.is_net_skins_paid:
                        subtotal += event.skins_fee
                    if reg.is_greens_fee_paid:
                        subtotal += event.green_fee
                    if reg.is_cart_fee_paid:
                        subtotal += event.cart_fee

                group.payment_amount = (subtotal + decimal.Decimal("0.30")) / (decimal.Decimal("1.0") - decimal.Decimal("0.029"))
                group.save()

                count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR("Failed to update {}:".format(group.id)))
                self.stderr.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS('Successfully updated {} groups'.format(count)))
