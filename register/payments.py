import stripe
import calendar
from datetime import datetime, timezone, timedelta
from django.conf import settings
from rest_framework.serializers import ValidationError

from register.exceptions import StripeCardError, StripePaymentError


def stripe_charge(user, event, amount_due, token):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    member = user.member
    customer_id = ""

    # scenario: member does not have a stripe customer id
    if (member.stripe_customer_id == "" or member.stripe_customer_id is None) and token != "no-token":
        customer = stripe.Customer.create(
            description=member.member_name(),
            email=user.email,
            source=token
        )
        customer_id = customer.stripe_id

        if member.save_last_card:
            member.stripe_customer_id = customer.stripe_id
            member.save()

    # scenario: member has stripe customer id but is using a new card
    elif member.stripe_customer_id != "" and member.stripe_customer_id is not None and token != "no-token":
        customer = stripe.Customer.retrieve(id=member.stripe_customer_id)
        customer.source = token
        customer.save()
        customer_id = customer.stripe_id

    # scenario: member has stripe customer id and using existing card (source)
    elif member.stripe_customer_id != "" and member.stripe_customer_id is not None and token == "no-token":
        customer_id = member.stripe_customer_id

    # invalid request
    else:
        raise ValidationError("Missing stripe id and/or stripe token")

    # Translate any Stripe error to an ApiException
    try:
        return create_stripe_charge(user, customer_id, event, amount_due)
    except stripe.error.CardError as e:
        raise StripeCardError(e)
    except stripe.error.RateLimitError as e:
        raise StripePaymentError(e)
    except stripe.error.InvalidRequestError as e:
        raise StripePaymentError(e)
    except stripe.error.AuthenticationError as e:
        raise StripePaymentError(e)
    except stripe.error.APIConnectionError as e:
        raise StripePaymentError(e)
    except stripe.error.StripeError as e:
        raise StripePaymentError(e)


def create_stripe_charge(user, customer_id, event, amount_due):

    charge_description = "{} ({}): {}".format(event.name, event.get_event_type_display(), event.start_date.strftime('%Y-%m-%d'))

    return stripe.Charge.create(
        amount=amount_due,
        currency="usd",
        customer=customer_id,
        receipt_email=user.email,
        description=charge_description,
        metadata={
            "event": event.name,
            "date": event.start_date.strftime('%Y-%m-%d'),
            "event_type": event.get_event_type_display(),
            "member": "{} {}".format(user.first_name, user.last_name),
            "email": user.email
        }
    )


def convert_tstamp(ts):
    tz = timezone.utc if settings.USE_TZ else None
    return datetime.fromtimestamp(ts, tz)


def get_stripe_charges(event):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    results = []
    start_dt = event.signup_start - timedelta(days=1)
    end_dt = event.signup_end + timedelta(days=1)
    params = {
        'limit': 100,
        'created[gte]': calendar.timegm(start_dt.timetuple()),
        'created[lte]': calendar.timegm(end_dt.timetuple())
    }
    filtered_charges = stripe.Charge.auto_paging_iter(**params)
    for charge in filtered_charges:
        results.append(charge)

    return results


def get_customer_charges(customer_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    results = []
    params = {
        'limit': 100,
        'customer': customer_id
    }
    filtered_charges = stripe.Charge.auto_paging_iter(**params)
    for charge in filtered_charges:
        results.append(charge)

    return results


def get_stripe_charge(charge_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Charge.retrieve(charge_id)
