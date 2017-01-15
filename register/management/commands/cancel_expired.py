from django.core.management.base import NoArgsCommand
from datetime import datetime
from register.models import RegistrationSlot, RegistrationGroup


class Command(NoArgsCommand):
    help = 'Find and clear pending registrations that have expired'

    def handle_noargs(self, **options):

        groups = RegistrationGroup.objects.filter(expires_lt=datetime.now()).filter(payment_confirmation_code="")
        count = len(groups)

        for group in groups:
            RegistrationSlot.objects \
                .filter(registration_group=group.id) \
                .filter(event__event_type="L") \
                .update(**{"status": "A", "registration_group": None, "member": None})

            # Delete non-league slots
            RegistrationSlot.objects. \
                filter(registration_group=group.id) \
                .exlude(event__event_type="L") \
                .delete()

            group.delete()

        self.stdout.write(self.style.SUCCESS('Cleared %s expired slots' % count))
