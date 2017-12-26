from datetime import timedelta, datetime
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Event, EventTemplate
from .serializers import EventSerializer, EventTemplateSerializer, EventDetailSerializer


class EventList(generics.ListAPIView):
    """ API endpoint to view Events
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        """ Optionally filter by year and month
        """
        queryset = Event.objects.all()
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)

        if year is not None:
            queryset = queryset.filter(start_date__year=year)
        if month is not None:
            queryset = queryset.filter(start_date__month=month)

        return queryset


class QuickEventList(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        today = datetime.today()
        start_date = today + timedelta(days=-7)
        end_date = today + timedelta(days=14)
        return Event.objects.all()\
            .filter(start_date__lte=end_date, start_date__gt=start_date)\
            .exclude(event_type="R")\
            .order_by('start_date')


class UpcomingEventList(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        today = datetime.today()
        queryset = Event.objects.all()
        queryset = queryset.filter(signup_start__lte=today, signup_end__gt=today)
        # print(queryset.query)
        return queryset


class EventDetail(generics.RetrieveDestroyAPIView):
    """ API endpoint to edit Clubs
    """
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer


class EventTemplateList(generics.ListCreateAPIView):
    """ API endpoint to view Events
    """
    queryset = EventTemplate.objects.all()
    serializer_class = EventTemplateSerializer


class EventTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint to edit Clubs
    """
    queryset = EventTemplate.objects.all()
    serializer_class = EventTemplateSerializer


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated,))
def update_portal(request, pk):

    event = get_object_or_404(Event, pk=pk)
    portal = request.data.get("portal", None)
    if portal is None:
        raise ValidationError("A portal url is required")

    event.portal_url = portal
    event.save()

    serializer = EventDetailSerializer(event, context={'request': request})
    return Response(serializer.data)
