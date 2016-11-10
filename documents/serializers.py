from events.serializers import EventSerializer
from .models import Document
from rest_framework import serializers


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    event = EventSerializer()

    class Meta:
        model = Document
        fields = ("url", "id", "title", "document_type", "file", "last_update", "event")
