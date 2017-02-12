import logging
import stripe
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from register.models import RegistrationSlot
from register.payments import get_customer_charges
from .models import Club, Member, SeasonSettings
from .serializers import ClubSerializer, MemberSerializer, UserDetailSerializer, SettingsSerializer

logger = logging.getLogger('core')


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def api_root(request):
    return Response({
        'settings': reverse('current-settings', request=request),
        'members': reverse('member-list', request=request),  # TODO: private
        'courses': reverse('course-list', request=request),
        'course-setups': reverse('coursesetup-list', request=request),
        'holes': reverse('hole-list', request=request),
        'course-setup-holes': reverse('coursesetuphole-list', request=request),
        'events': reverse('event-list', request=request),
        'event-templates': reverse('eventtemplate-list', request=request),
        'policies': reverse('policy-list', request=request),
        'announcements': reverse('announcement-list', request=request),
        'documents': reverse('document-list', request=request),  # TODO: private
    })


class ClubList(generics.ListAPIView):
    """ API endpoint to view Clubs
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubDetail(generics.RetrieveUpdateAPIView):
    """ API endpoint to edit Clubs
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class SettingsList(generics.ListAPIView):
    """ API endpoint to view Clubs
    """
    queryset = SeasonSettings.objects.all()
    serializer_class = SettingsSerializer


class MemberList(generics.ListAPIView):
    """ API endpoint to view Members
    """
    # queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        """ Optionally filter by year
        """
        queryset = Member.objects.all()
        is_registered = self.request.query_params.get('registered', None)

        if is_registered is not None:
            ss = SeasonSettings.objects.current_settings()
            ids = RegistrationSlot.objects.members(ss.reg_event_id)
            queryset = queryset.filter(pk__in=ids)

        return queryset


class MemberDetail(generics.RetrieveAPIView):
    """ API endpoint to view a single Member
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


@api_view(['GET', ])
def current_settings(request):
    cs = SeasonSettings.objects.current_settings()
    serializer = SettingsSerializer(cs, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', ])
def is_available(request):
    # TODO: throttle this endpoint
    email = request.query_params.get('e', None)
    username = request.query_params.get('u', None)

    if email is not None:
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response(status=204)
    elif username is not None:
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(status=204)

    return Response(data={'detail': 'unavailable'}, status=409)


@api_view(['POST', ])
def register_new_member(request):
    serializer = UserDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=204)
    return Response(data=serializer.errors, status=400)


# TODO: friends should be made restful (child of member?)
@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def friends(request):
    """ API endpoint to view the current member's favorites
    """
    member = get_object_or_404(Member, pk=request.user.member.id)
    serializer = MemberSerializer(member.favorites, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
def add_friend(request, member_id):
    member = get_object_or_404(Member, pk=request.user.member.id)
    friend = get_object_or_404(Member, pk=member_id)
    member.favorites.add(friend)
    member.save()
    serializer = MemberSerializer(member.favorites, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
def remove_friend(request, member_id):
    member = get_object_or_404(Member, pk=request.user.member.id)
    friend = get_object_or_404(Member, pk=member_id)
    member.favorites.remove(friend)
    member.save()
    serializer = MemberSerializer(member.favorites, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def stripe_details(request):
    """ API endpoint to view the current member's stripe account details
    """
    member = get_object_or_404(Member, pk=request.user.member.id)
    if member.stripe_customer_id is None or member.stripe_customer_id == "":
        return Response({
            "stripe_id": "",
            "card": "",
            "expires": ""
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer = stripe.Customer.retrieve(id=member.stripe_customer_id)
    default_source = customer.sources.data[0]
    card = "{} ending in {}".format(default_source.brand, default_source.last4)
    expires = "{}/{}".format(default_source.exp_month, default_source.exp_year)

    # TODO: change the id here to the card id
    return Response({
        "stripe_id": customer.id,
        "card": card,
        "expires": expires
    })


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def stripe_charges(request):
    customer_id = request.query_params.get('id', None)
    if customer_id is None:
        customer_id = request.user.member.stripe_customer_id
    charges = get_customer_charges(customer_id)
    return Response(charges)
