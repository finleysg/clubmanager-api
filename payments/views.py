import stripe
import logging
from datetime import datetime, timezone
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from events.models import Event
from .models import Charge


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
def pay(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    event = get_object_or_404(Event, pk=request.event_id)
    member = request.user.member
    charge_description = "Payment for {} by {}".format(event.name, member.member_name())
    result = "Your payment of {} was processed successfully"

    try:
        charge = stripe.Charge.create(
            amount=request.amount_due,
            currency="usd",
            customer=member.stripe_customer_id,
            source=request.token,
            receipt_email=request.user.email,
            description=charge_description,
            metadata={"event": event.name, "member": member.member_name, "email": request.user.email}
        )

        transaction = Charge(stripe_id=charge.id, member=member, event=event,
                             source=request.token, amount=request.amount_due, description=charge_description,
                             paid=charge.paid, captured=charge.captured, receipt_sent=charge.receipt_email is None,
                             status=charge.status, charge_created=convert_tstamp(charge.created))
        transaction.save()

    except stripe.error.CardError as e:
        body = e.json_body
        err = body['error']
        log_error(result, e)
        result = err['message']
    except stripe.error.RateLimitError as e:
        log_error("Too many requests made to the API too quickly", e)
        result = "The Stripe system is busy. Please try again in a few minutes."
    except stripe.error.InvalidRequestError as e:
        log_error("Invalid parameters were supplied to Stripe's API", e)
        result = "A system problem prevented your payment from going through."
    except stripe.error.AuthenticationError as e:
        log_error("Authentication with Stripe's API failed - maybe you changed API keys recently", e)
        result = "A system problem prevented your payment from going through."
    except stripe.error.APIConnectionError as e:
        log_error("Network communication with Stripe failed", e)
        result = "The Stripe system is busy. Please try again in a few minutes."
    except stripe.error.StripeError as e:
        log_error("Stripe system error", e)
        result = "A system problem prevented your payment from going through."
    except Exception as e:
        log_error("Exception unrelated to Stripe", e)
        result = "A system problem prevented your payment from going through."

    return Response(result)


def convert_tstamp(ts):
    tz = timezone.utc if settings.USE_TZ else None
    return datetime.fromtimestamp(ts, tz)


def log_error(message, e):
    logger = logging.getLogger("stripe.payments")
    logger.error(message)
    logger.exception(e)
