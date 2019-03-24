import stripe
import calendar
from datetime import datetime, timezone, timedelta
from django.conf import settings
from rest_framework.serializers import ValidationError
from .models import RegistrationRefund
from .exceptions import StripeCardError, StripePaymentError


def stripe_charge(user, event, amount_due, token):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    member = user.member

    try:

        # badly named "save_last_card" == use a saved card
        if member.save_last_card and member.has_stripe_id() and token == "no-token":
            return stripe_customer_charge(user, member.stripe_customer_id, event, amount_due)

        elif token != "no-token":
            return stripe_token_charge(user, token, event, amount_due)

        else:
            raise ValidationError("Missing stripe id and/or stripe token")

    # Translate any Stripe error to an ApiException
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
    # TODO: maybe some general payment error with useful messaging
    # except Exception as ex:
    #     raise ApiException()


def stripe_customer_charge(user, customer_id, event, amount_due):

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


# This version uses source - no customer
def stripe_token_charge(user, token, event, amount_due):

    charge_description = "{} ({}): {}".format(event.name, event.get_event_type_display(), event.start_date.strftime('%Y-%m-%d'))

    return stripe.Charge.create(
        amount=amount_due,
        currency="usd",
        source=token,
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


def refund_stripe_charge(charge, amount):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if not amount or amount == 0:
        return stripe.Charge.refund(charge)  # full refund
    else:
        return stripe.Charge.refund(charge, amount)


def refund_payment(record_id, record_type, payment_code, amount, member, reason):
    charge = get_stripe_charge(payment_code)
    refund = refund_stripe_charge(charge, amount)
    refund_record = RegistrationRefund(related_record_id=record_id, related_record_name=record_type,
                                       recorded_by=member, refund_code=refund.stripe_id, refund_amount=refund.amount / 100,
                                       comment=reason)
    refund_record.save()
    return refund_record
