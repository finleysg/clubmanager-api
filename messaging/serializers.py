from .models import Announcement
from rest_framework import serializers


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):

    event_id = serializers.CharField(source="event.id")
    event_name = serializers.CharField(source="event.name")
    document_name = serializers.CharField(source="document.title")
    document_url = serializers.CharField(source="document.file.url")

    class Meta:
        model = Announcement
        fields = ("url", "id", "text", "starts", "expires",
                  "event_id", "event_name", "external_url", "external_name",
                  "document_name", "document_url", "title", 'members_only', )
