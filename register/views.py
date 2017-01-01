import stripe
import logging

from datetime import datetime, timezone
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from courses.models import CourseSetupHole
from .exceptions import StripeCardError, StripePaymentError
from .models import RegistrationSlot, RegistrationGroup
from .serializers import RegistrationSlotSerializer, RegistrationGroupSerializer
from .event_reservation import create_event

from core.models import Member
from events.models import Event


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def registrations(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    results = RegistrationSlot.objects.filter(event=event)
    serializer = RegistrationSlotSerializer(results, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET, '])
@permission_classes((permissions.IsAuthenticated,))
def registration_group(request, group_id):
    # group = get_object_or_404(RegistrationGroup, pk=group_id)
    group = RegistrationGroup.objects.filter(pk=group_id)
    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def reserve(request):

    event_id = request.data["event_id"]
    course_setup_hole_id = request.data.get("course_setup_hole_id", None)
    slot_ids = request.data.get("slot_ids", None)
    starting_order = request.data.get("starting_order", 0)

    member = get_object_or_404(Member, pk=request.user.member.id)
    event = get_object_or_404(Event, pk=event_id)

    reg_event = create_event(event)
    group = reg_event.reserve(member, **{
        "slot_ids": slot_ids,
        "course_setup_hole_id": course_setup_hole_id,
        "starting_order": starting_order
    })

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def register(request):

    group_tmp = request.data["group"]
    amount_due = float(group_tmp["payment_amount"])
    verification_token = group_tmp["card_verification_token"]
    if verification_token is None or verification_token == "":
        verification_token = "no-token"

    event = get_object_or_404(Event, pk=group_tmp["event"])
    group = get_object_or_404(RegistrationGroup, pk=group_tmp["id"], signed_up_by=request.user.member)

    charge = stripe_charge(request.user, event, int(amount_due * 100), verification_token)

    group.payment_amount = amount_due
    group.card_verification_token = verification_token
    group.payment_confirmation_code = charge.id
    group.payment_confirmation_timestamp = tz.now()
    group.notes = group_tmp["notes"]
    group.save()

    for slot_tmp in group_tmp["slots"]:
        slot = RegistrationSlot.objects.get(pk=slot_tmp["id"])
        member = Member.objects.get(pk=slot_tmp["member"])
        slot.member = member
        slot.expires = None
        slot.status = "R"
        slot.is_event_fee_paid = slot_tmp.get("is_event_fee_paid", True)
        slot.is_gross_skins_paid = slot_tmp.get("is_gross_skins_paid", False)
        slot.is_net_skins_paid = slot_tmp.get("is_net_skins_paid", False)
        slot.is_greens_fee_paid = slot_tmp.get("is_greens_fee_paid", False)
        slot.is_cart_fee_paid = slot_tmp.get("is_cart_fee_paid", False)
        slot.save()

    serializer = RegistrationGroupSerializer(group, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def cancel_reserved_slots(request):

    group_id = request.data["group_id"]
    group = get_object_or_404(RegistrationGroup, pk=group_id, signed_up_by=request.user.member)
    event = get_object_or_404(Event, pk=group.event.id)

    RegistrationSlot.objects.cancel_group(event, group)

    return Response(status=204)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny,))
def cancel_expired_slots(request):

    RegistrationSlot.objects.cancel_expired()

    return Response(status=204)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def add_row(request):

    event_id = request.data["event_id"]
    course_setup_hole_id = request.data["course_setup_hole_id"]
    event = get_object_or_404(Event, pk=event_id)
    hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)

    new_slots = RegistrationSlot.objects.add_slots(event, hole)

    serializer = RegistrationSlotSerializer(new_slots, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def remove_row(request):

    event_id = request.data["event_id"]
    course_setup_hole_id = request.data["course_setup_hole_id"]
    starting_order = request.data["starting_order"]
    event = get_object_or_404(Event, pk=event_id)
    hole = get_object_or_404(CourseSetupHole, pk=course_setup_hole_id)

    RegistrationSlot.objects.remove_hole(event, hole, starting_order)

    return Response(status=204)


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
        raise StripePaymentError("Missing stripe id and/or stripe token")

    return create_stripe_charge(user, customer_id, event, amount_due)


def create_stripe_charge(user, customer_id, event, amount_due):

    charge_description = "{} ({}): {}".format(event.name, event.get_event_type_display(), event.start_date.strftime('%Y-%m-%d'))

    try:
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
