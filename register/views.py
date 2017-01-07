import stripe
import logging
import threading

from datetime import datetime, timezone
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from courses.models import CourseSetupHole
from .exceptions import StripeCardError, StripePaymentError, SlotConflictError
from .models import RegistrationSlot, RegistrationGroup
from .serializers import RegistrationSlotSerializer, RegistrationGroupSerializer
from .event_reservation import create_event

from core.models import Member
from events.models import Event
from .registration_cache import can_reserve, reserve_slots, clear_slots, clear_slot

reserve_lock = threading.Lock()


@permission_classes((permissions.IsAuthenticated,))
class RegistrationGroupDetail(generics.RetrieveAPIView):
    """ API endpoint to view Registration Groups
    """
    queryset = RegistrationGroup.objects.all()
    serializer_class = RegistrationGroupSerializer


@permission_classes((permissions.IsAuthenticated,))
class RegistrationList(generics.ListAPIView):

    serializer_class = RegistrationSlotSerializer

    def get_queryset(self):
        """
        Optionally restricts the list of registrations for a given event.
        """
        queryset = RegistrationSlot.objects.all()
        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            event = get_object_or_404(Event, pk=event_id)
            queryset = queryset.filter(event=event)
        return queryset


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def registrations(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    results = RegistrationSlot.objects.filter(event=event)
    serializer = RegistrationSlotSerializer(results, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
@transaction.atomic()
def reserve(request):

    member = Member.objects.filter(pk=request.user.member.id).get()

    event_id = request.data.get("event_id", 0)
    if event_id == 0:
        raise ValidationError("There was no event id passed")

    event = Event.objects.filter(pk=event_id).get()
    if event is None:
        raise ValidationError("{} is not a valid event id".format(event_id))

    if event.registration_window() != "registration":  # and not request.user.is_staff:
        raise ValidationError("Event {} is not open for registration".format(event_id))

    # TODO: validation expiration

    course_setup_hole_id = request.data.get("course_setup_hole_id", None)
    slot_ids = request.data.get("slot_ids", None)
    starting_order = request.data.get("starting_order", 0)

    # with reserve_lock:
    #     if not can_reserve(event.id, slot_ids):
    #         raise SlotConflictError()
    #     reserve_slots(event.id, slot_ids)

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
def register(request):

    group_tmp = request.data.get("group", None)
    if group_tmp is None:
        raise ValidationError("You neglected to submit a registration group")

    event = Event.objects.filter(pk=group_tmp["event"]).get()
    if event is None:
        raise ValidationError("{} is not a valid event id".format(group_tmp["event"]))

    group = RegistrationGroup.objects.filter(pk=group_tmp["id"]).get()
    if group is None:
        raise ValidationError("{} is not a valid group id".format(group_tmp["id"]))

    # TODO: validate the payment amount

    amount_due = float(group_tmp["payment_amount"])
    verification_token = group_tmp["card_verification_token"]
    if verification_token is None or verification_token == "":
        verification_token = "no-token"

    try:
        charge = stripe_charge(request.user, event, int(amount_due * 100), verification_token)
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

    group.payment_amount = amount_due
    group.card_verification_token = verification_token
    group.payment_confirmation_code = charge.id
    group.payment_confirmation_timestamp = tz.now()
    group.notes = group_tmp["notes"]
    group.save()

    for slot_tmp in group_tmp["slots"]:
        slot = RegistrationSlot.objects.select_for_update().get(pk=slot_tmp["id"])
        member = Member.objects.get(pk=slot_tmp["member"])
        if member is None:
            raise ValidationError("{} is an invalid member id".format(slot_tmp["member"]))

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

    group_id = request.data.get("group_id", 0)
    if group_id == 0:
        raise ValidationError("Missing group id")

    group = RegistrationGroup.objects.filter(pk=group_id).get()
    if group is None:
        raise ValidationError("{} is an invalid group id".format(group_id))

    # slot_ids = RegistrationSlot.objects.select_for_update().filter(registration_group__exact=group_id).values_list('pk', flat=True)
    # with reserve_lock:
    #     clear_slots(group.event.id, slot_ids)

    RegistrationSlot.objects.cancel_group(group)

    return Response(status=204)


def cancel_expired_slots():

    slots = list(RegistrationSlot.objects.filter(status="P").filter(expires__lt=datetime.now()))
    if slots is not None and len(slots) > 0:
        RegistrationSlot.objects.cancel_expired()
        # with reserve_lock:
        #     for slot in slots:
        #         clear_slot(slot.event, slot.id)

    return len(slots)


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
        raise ValidationError("Missing stripe id and/or stripe token")

    return create_stripe_charge(user, customer_id, event, amount_due)


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


def log_error(message, e):
    logger = logging.getLogger("stripe.payments")
    logger.error(message)
    logger.exception(e)
