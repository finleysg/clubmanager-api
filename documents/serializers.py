from events.serializers import EventSerializer
from .models import Document
from rest_framework import serializers


class DocumentDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ("year", "title", "document_type", "file", "event", "last_update", )
        read_only_fields = ("id", )


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    event = EventSerializer()

    class Meta:
        model = Document
        fields = ("year", "id", "title", "document_type", "file", "last_update", "event")
