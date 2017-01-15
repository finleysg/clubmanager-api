from templated_email import send_templated_mail


def send_new_member_welcome():
    send_templated_mail(
        template_name='welcome',
        from_email='from@example.com',
        recipient_list=['to@example.com'],
        # context={
        #     'username':request.user.username,
        #     'full_name':request.user.get_full_name(),
        #     'signup_date':request.user.date_joined
        # },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )


def send_new_member_notification(user, group):
    send_templated_mail(
        template_name='new_member',
        from_email='admin@bhmc.org',
        recipient_list=['finleysg@gmail.com'],
        context={
            'name': "{} {}".format(user.first_name, user.last_name),
            'email': user.email,
            'ghin': user.member.ghin,
            'signup_date': user.date_joined,
            'former_club': group.notes.replace('NEW MEMBER REGISTRATION', '')
        },
    )


def send_registration_confirmation():
    send_templated_mail(
        template_name='welcome',
        from_email='from@example.com',
        recipient_list=['to@example.com'],
        # context={
        #     'username':request.user.username,
        #     'full_name':request.user.get_full_name(),
        #     'signup_date':request.user.date_joined
        # },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )


def send_league_confirmation():
    send_templated_mail(
        template_name='welcome',
        from_email='from@example.com',
        recipient_list=['to@example.com'],
        # context={
        #     'username':request.user.username,
        #     'full_name':request.user.get_full_name(),
        #     'signup_date':request.user.date_joined
        # },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )


def send_payment_confirmation():
    send_templated_mail(
        template_name='welcome',
        from_email='from@example.com',
        recipient_list=['to@example.com'],
        # context={
        #     'username':request.user.username,
        #     'full_name':request.user.get_full_name(),
        #     'signup_date':request.user.date_joined
        # },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )
