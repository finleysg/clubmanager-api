import stripe
import logging
from datetime import datetime, timezone
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from django.db import transaction
from events.models import Event
from payments.exceptions import StripeCardError, StripePaymentError
from signup.models import RegistrationGroup, SignupSlot
from signup.serializers import RegistrationGroupSerializer
from .models import Charge


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
@transaction.atomic()
def pay(request):

    event_id = request.data["event_id"]
    group_id = request.data["group_id"]
    # Stripe wants the amount in cents
    amount_due = int(float(request.data["amount_due"]) * 100)  # TODO: make sure this is right
    token = request.data["token"]

    member = request.user.member
    event = get_object_or_404(Event, pk=event_id)

    charge = create_stripe_charge(amount_due, request.user.email, event, member, token)

    charge_local = Charge(stripe_id=charge.id, member=member, event=event,
                          source=token, amount=amount_due / 100, description=charge.description,
                          paid=charge.paid, captured=charge.captured, receipt_sent=charge.receipt_email is None,
                          status=charge.status, charge_created=convert_tstamp(charge.created))
    charge_local.save()

    group = get_object_or_404(RegistrationGroup, pk=group_id, signed_up_by=member)
    group.payment_confirmation_code = charge.id
    group.save()

    slots = get_list_or_404(SignupSlot, registration_group_id=group_id)
    for slot in slots:
        slot.status = "R"
        slot.save()

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


def create_stripe_charge(amount_due, email, event, member, token):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    description = "Payment for {} by {}".format(event.name, member.member_name())

    try:
        if token is None:
            # TODO: raise error if missing stripe_customer_id
            return stripe.Charge.create(
                amount=amount_due,
                currency="usd",
                customer=member.stripe_customer_id,
                receipt_email=email,
                description=description,
                metadata={"event": event.name, "member": member.member_name(), "email": email}
            )
        else:
            return stripe.Charge.create(
                amount=amount_due,
                currency="usd",
                source=token,
                receipt_email=email,
                description=description,
                metadata={"event": event.name, "member": member.member_name(), "email": email}
            )
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


def convert_tstamp(ts):
    tz = timezone.utc if settings.USE_TZ else None
    return datetime.fromtimestamp(ts, tz)


def log_error(message, e):
    logger = logging.getLogger("stripe.payments")
    logger.error(message)
    logger.exception(e)
