from .models import Announcement, Contact
from events.serializers import EventSerializer, SimpleEventSerializer
from documents.serializers import DocumentSerializer
from rest_framework import serializers


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):

    event = SimpleEventSerializer(required=False)
    document = DocumentSerializer(required=False)
    # event_id = serializers.CharField(source="event.id")
    # event_name = serializers.CharField(source="event.name")
    # document_name = serializers.CharField(source="document.title")
    # document_url = serializers.CharField(source="document.file.url")

    class Meta:
        model = Announcement
        fields = ("url", "id", "text", "starts", "expires",
                  "event", "document", "external_url", "external_name",
                  "title", 'members_only', )


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("president_name", "president_phone", "vice_president_name", "vice_president_phone",
                  "secretary_name", "secretary_phone", "treasurer_name", "treasurer_phone",
                  "directors", "committees", "staff", )
