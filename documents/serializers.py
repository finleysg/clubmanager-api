from events.serializers import EventSerializer
from events.models import Event
from .models import Document
from rest_framework import serializers


class DocumentDetailSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = Document
        fields = ("id", "year", "title", "document_type", "file", "event", "last_update", )

    def create(self, validated_data):
        event = validated_data.get('event', None)
        year = validated_data.pop('year')
        title = validated_data.pop('title')
        document_type = validated_data.pop('document_type')
        file = validated_data.pop('file')

        doc = Document(year=year, title=title, document_type=document_type, file=file, event=event)
        doc.save()
        return doc

    def update(self, instance, validated_data):
        instance.file = validated_data.get('file', instance.file)
        instance.document_type = validated_data.get('document_type', instance.document_type)
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.event = validated_data.get('event', instance.event)
        instance.save()

        return instance


class DocumentSerializer(serializers.ModelSerializer):

    event = EventSerializer()

    class Meta:
        model = Document
        fields = ("year", "id", "title", "document_type", "file", "last_update", "event")
