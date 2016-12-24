from rest_framework import generics
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.decorators import api_view

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


@api_view(['POST', ])
def contact_message(request):
    send_mail(
        "BHMC: Contact Us Message from " + request.data["full_name"],
        request.data["message_text"],
        request.data["email"],
        ["finleysg@gmail.com"]
    )
