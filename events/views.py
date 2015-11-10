from rest_framework import generics

from .models import Event, EventTemplate
from .serializers import EventSerializer, EventTemplateSerializer


class EventList(generics.ListCreateAPIView):
    """ API endpoint to view Events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint to edit Clubs
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


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
