from rest_framework import generics
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Announcement, ContactMessage
from .serializers import AnnouncementSerializer


class AnnouncementDetail(generics.RetrieveAPIView):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    
    
class AnnouncementList(generics.ListAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        today = timezone.now()
        queryset = Announcement.objects.all()
        queryset = queryset.filter(starts__lte=today, expires__gte=today)
        return queryset


@api_view(['POST', ])
@permission_classes((permissions.AllowAny,))
def contact_message(request):
    sender = request.data["full_name"]
    sender_email = request.data["email"]
    message_text = request.data["message_text"]
    message = ContactMessage(full_name=sender, email=sender_email, message_text=message_text)
    message.save()

    send_mail(
        "BHMC: Contact Us Message from " + sender,
        message_text,
        sender_email,
        ["contact@bhmc.com"]
    )

    return Response(status=201)

