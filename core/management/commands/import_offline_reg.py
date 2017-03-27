from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from register.models import RegistrationGroup, RegistrationSlot
from events.models import Event


class Command(BaseCommand):
    help = 'Create season registration records from all members not already registered'

    def handle(self, *args, **options):
        count = 0
        dups = 0
        event = Event.objects.get(pk=46)  # TODO: use settings
        users = User.objects.filter(is_active=True)

        for user in users:
            member = user.member
            try:
                RegistrationSlot.objects.get(event=event, member=member)
                dups += 1
            except:
                try:
                    group = RegistrationGroup(event=event, signed_up_by=member, payment_confirmation_code="offline",
                                              payment_confirmation_timestamp=dt_reserved, payment_amount=98.00,
                                              notes="Imported from existing system - online registration")
                    group.save()
                    print("group_id = {}".format(group.id))
                    slot = RegistrationSlot(event=event, registration_group=group, member=member, status="R",
                                            is_event_fee_paid=True)
                    slot.save()
                except Exception as e:
                    print(e)
                    print("error for {} {}".format(user.first_name, user.last_name))

            count += 1

        self.stdout.write(self.style.SUCCESS('Successfully registered %s members with %s skipped (already registered)' % (count, dups)))
