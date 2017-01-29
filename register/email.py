import os
from decimal import Decimal
from django.conf import settings
from templated_email import send_templated_mail
from templated_email import InlineImage
from register.models import RegistrationSlot

sender_email = "BHMC (testing)<admin@zoomdoggydesign.com>"
secretary_email = "nate55792@gmail.com"
treasurer_email = "pmwright21@gmail.com"

logo_file = os.path.join(settings.BASE_DIR, 'templates/templated_email/logo.png')
with open(logo_file, 'rb') as logo:
    image = logo.read()
    inline_image = InlineImage(filename=logo_file, content=image)


def send_new_member_welcome(user, config):
    send_templated_mail(
        template_name='welcome.html',
        from_email=sender_email,
        recipient_list=[user.email],
        context={
            'first_name': user.first_name,
            'year': config.year,
            'login_url': '{}/member/login'.format(config.website_url),
            'account_url': '{}/member/account'.format(config.website_url),
            'matchplay_url': '{}/events/{}/matchplay'.format(config.website_url, config.match_play_event.id),
            'logo_image': inline_image
        },
        template_suffix='html',
        headers={"Reply-To": "no-reply@zoomdoggydesign.com"}
    )


def send_returning_member_welcome(user, config):
    send_templated_mail(
        template_name='welcome_back.html',
        from_email=sender_email,
        recipient_list=[user.email],
        context={
            'first_name': user.first_name,
            'year': config.year,
            'account_url': '{}/member/account'.format(config.website_url),
            'matchplay_url': '{}/events/{}/matchplay'.format(config.website_url, config.match_play_event.id),
            'logo_image': inline_image
        },
        template_suffix='html',
        headers={"Reply-To": "no-reply@zoomdoggydesign.com"}
    )


def send_new_member_notification(user, group, config):
    send_templated_mail(
        template_name='new_member_notification',
        from_email=sender_email,
        recipient_list=[treasurer_email, secretary_email],
        context={
            'name': '{} {}'.format(user.first_name, user.last_name),
            'email': user.email,
            'ghin': user.member.ghin,
            'club': group.notes.replace('NEW MEMBER REGISTRATION', ''),
            'admin_url': '{}/auth/user/?q={}'.format(config.admin_url, user.username),
            'logo_image': inline_image
        },
        template_suffix='html',
        headers={"Reply-To": "no-reply@zoomdoggydesign.com"}
    )


def send_has_notes_notification(user, group, event):
    if group.notes is not None and group.notes != '':
        send_templated_mail(
            template_name='has_notes_notification',
            from_email=sender_email,
            recipient_list=[treasurer_email, secretary_email],
            context={
                'name': '{} {}'.format(user.first_name, user.last_name),
                'email': user.email,
                'event': event.name,
                'notes': group.notes,
                'logo_image': inline_image
            },
            template_suffix='html',
            headers={"Reply-To": "no-reply@zoomdoggydesign.com"}
        )


def send_event_confirmation(user, group, event, config):

    registrations = list(RegistrationSlot.objects.filter(registration_group=group))
    required_fees = get_required_fees(event, registrations)
    optional_fees = get_optional_fees(event, registrations)

    email_context = {
        'user_name': '{} {}'.format(user.first_name, user.last_name),
        'event_name': event.name,
        'event_date': event.start_date,
        'event_start': event.start_time,
        'event_hole': get_starting_hole(event, group),
        'required_fees': required_fees,
        'optional_fees': optional_fees,
        'transaction_fees': Decimal(str(group.payment_amount)) - (required_fees + optional_fees),
        'total_fees': group.payment_amount,
        'payment_confirmation_code': group.payment_confirmation_code,
        'show_confirmation_code': True,
        'members': get_members(event, registrations),
        'event_url': '{}/events/{}/detail'.format(config.website_url, event.id),
        'logo_image': inline_image
    }

    send_templated_mail(
        template_name='registration_confirmation.html',
        from_email=sender_email,
        recipient_list=[user.email],
        context=email_context,
        template_suffix='html',
        headers={"Reply-To": "no-reply@zoomdoggydesign.com"}
    )

    # remove payment conf code before sending the rest
    email_context['show_confirmation_code'] = False
    recipients = get_recipients(user, registrations)

    if len(recipients) > 0:
        send_templated_mail(
            template_name='registration_confirmation.html',
            from_email=sender_email,
            recipient_list=recipients,
            context=email_context,
            template_suffix='html',
            headers={"Reply-To": "no-reply@zoomdoggydesign.com"}
        )


def get_starting_hole(event, group):
    if event.event_type == 'L':
        course_name = group.course_setup.name.replace(' League', '')
        if group.starting_order == 0:
            return '{} {}A'.format(course_name, group.starting_hole)
        else:
            return '{} {}B'.format(course_name, group.starting_hole)

    return 'Tee times'


def get_required_fees(event, registrations):
    fees = Decimal('0.0')
    for reg in registrations:
        fees = fees + event.event_fee

    return fees


def get_optional_fees(event, registrations):
    fees = Decimal('0.0')
    for reg in registrations:
        if reg.is_gross_skins_paid:
            fees = fees + event.skins_fee
        if reg.is_net_skins_paid:
            fees = fees + event.skins_fee
        if reg.is_greens_fee_paid:
            fees = fees + event.green_fee
        if reg.is_cart_fee_paid:
            fees = fees + event.cart_fee

    return fees


def get_members(event, registrations):
    members = []
    for reg in registrations:
        members.append({
            'name': reg.member.member_name(),
            'email': reg.member.member_email(),
            'fees': get_fees(reg, event)
        })
    return members


def get_fees(registration, event):
    fees = [{
        'description': 'Event Fee',
        'amount': event.event_fee
    }]
    if registration.is_gross_skins_paid:
        fees.append({
            'description': 'Gross Skins',
            'amount': event.skins_fee
        })
    if registration.is_net_skins_paid:
        fees.append({
            'description': 'Net Skins',
            'amount': event.skins_fee
        })
    if registration.is_greens_fee_paid:
        fees.append({
            'description': 'Green Fee',
            'amount': event.green_fee
        })
    if registration.is_cart_fee_paid:
        fees.append({
            'description': 'Cart Fee',
            'amount': event.cart_fee
        })
    return fees


def get_recipients(user, registrations):
    recipients = []
    for reg in registrations:
        if reg.member.id != user.member.id:
            recipients.append(reg.member.member_email())

    return recipients
