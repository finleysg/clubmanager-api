import stripe
import logging

from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .exceptions import StripeCardError, StripePaymentError
from .models import SignupSlot, RegistrationGroup, Registration, Charge
from .serializers import SignupSlotSerializer, RegistrationGroupSerializer, RegistrationSerializer

from core.models import Member
from events.models import Event
from courses.models import CourseSetupHole


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def registrations(request, event_id):
    result = get_list_or_404(Registration, registration_group__event_id=event_id)
    serializer = RegistrationSerializer(result, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def registration_slots(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    slots = SignupSlot.objects.filter(event=event)

    serializer = SignupSlotSerializer(slots, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def reserve_slots(request):

    course_setup_hole_id = request.data["course_setup_hole_id"]
    slot_ids = request.data["slot_ids"]
    starting_order = request.data["starting_order"]
    event_id = request.data["event_id"]

    member = get_object_or_404(Member, pk=request.user.id)
    event = get_object_or_404(Event, pk=event_id)
    hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)

    slots = SignupSlot.objects.filter(pk__in=slot_ids)
    for slot in slots:
        if slot.status != "A":
            return HttpResponseBadRequest("One or more of the signup slots you requested are no longer available.")

    group = RegistrationGroup(event=event, course_setup=hole.course_setup, signed_up_by=request.user.member,
                              starting_hole=hole.hole_number, starting_order=starting_order)
    group.save()

    for i, slot in enumerate(slots):
        slot.status = "P"
        slot.registration_group = group
        slot.course_setup_hole = hole
        slot.expires = datetime.now() + timedelta(minutes=10)
        if i == 0:
            slot.member = member
        slot.save()

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def register(request):

    group_tmp = request.data["group"]

    group = get_object_or_404(RegistrationGroup, pk=group_tmp["id"], signed_up_by=request.user.member)
    group.payment_amount = group_tmp["payment_amount"]
    group.save()

    for slot_tmp in group_tmp["slots"]:
        slot = SignupSlot.objects.get(pk=slot_tmp["id"])
        member = Member.objects.get(pk=slot_tmp["member"])
        slot.member = member
        slot.save()
        registration = Registration(registration_group=group, member=member,
                                    is_event_fee_paid=slot_tmp["include_event_fee"],
                                    is_gross_skins_paid=slot_tmp["include_gross_skins"],
                                    is_net_skins_paid=slot_tmp["include_skins"])
        registration.save()

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def cancel_reserved_slots(request):

    group_id = request.data["group_id"]
    group = get_object_or_404(RegistrationGroup, pk=group_id, signed_up_by=request.user.member)
    SignupSlot.objects.cancel_group(group)
    group.delete()

    return Response(status=204)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny,))
def cancel_expired_slots(request):

    SignupSlot.objects.cancel_expired()

    return Response(status=204)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
@transaction.atomic()
def process_payment(request):

    event_id = request.data["event_id"]
    group_id = request.data["group_id"]
    amount_due = int(float(request.data["amount_due"]) * 100)  # Stripe wants the amount in cents
    token = request.data["token"]
    member = request.user.member

    event = get_object_or_404(Event, pk=event_id)
    charge = stripe_charge(request.user, event, amount_due, token)

    # charge_local = Charge(stripe_id=charge.id, member=member, event=event,
    #                       source=token, amount=amount_due / 100, description=charge.description,
    #                       paid=charge.paid, captured=charge.captured, receipt_sent=charge.receipt_email is None,
    #                       status=charge.status, charge_created=convert_tstamp(charge.created))
    # charge_local.save()

    group = get_object_or_404(RegistrationGroup, pk=group_id, signed_up_by=member)
    group.payment_confirmation_code = charge.id
    group.save()

    slots = get_list_or_404(SignupSlot, registration_group_id=group_id)
    for slot in slots:
        slot.expires = None
        slot.status = "R"
        slot.save()

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


def stripe_charge(user, event, amount_due, token):

    member = get_object_or_404(Member, pk=user.id)

    # scenario: member does not have a stripe customer id
    if member.stripe_customer_id is None and token is not None:
        customer = stripe.Customer.create(
            description=member.member_name(),
            email=user.email,
            source=token
        )
        member.stripe_customer_id = customer.stripe_id
        member.save()

    # scenario: member has stripe customer id but is using a new card
    elif member.stripe_customer_id is not None and token is not None:
        customer = stripe.Customer.retrieve(id=member.stripe_customer_id)
        customer.source = token
        customer.save()

    # scenario: member has stripe customer id and using existing card (source)
    elif member.stripe_customer_id is not None and token is None:
        pass

    # invalid request
    else:
        raise StripePaymentError("Missing stripe id and/or stripe token")

    return create_stripe_charge(user, event, amount_due)


def create_stripe_charge(user, event, amount_due):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    charge_description = "Payment for {} by {}".format(event.name, user.member_name())

    try:
        return stripe.Charge.create(
            amount=amount_due,
            currency="usd",
            customer=user.member.stripe_customer_id,
            receipt_email=user.email,
            description=charge_description,
            metadata={"event": event.name, "date": event.start_date.strftime('%Y-%m-%d')}
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
