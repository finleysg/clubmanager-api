from rest_framework import generics
from django.utils import timezone

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementDetail(generics.RetrieveAPIView):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    
    
class AnnouncementList(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    # queryset = Announcement.objects.all()

    def get_queryset(self):
        today = timezone.now()
        queryset = Announcement.objects.all()
        queryset = queryset.filter(starts__lte=today, expires__gte=today)
        return queryset
