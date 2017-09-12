from events.serializers import EventSerializer
from events.models import Event
from .models import Document, Sponsor, Photo
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


class PhotoDetailSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = Photo
        fields = ("id", "year", "title", "photo_type", "file", "event", "last_update", )

    def create(self, validated_data):
        event = validated_data.get('event', None)
        year = validated_data.pop('year')
        title = validated_data.pop('title')
        photo_type = validated_data.pop('photo_type')
        file = validated_data.pop('file')

        pic = Photo(year=year, title=title, photo_type=photo_type, file=file, event=event)
        pic.save()
        return pic

    def update(self, instance, validated_data):
        instance.file = validated_data.get('file', instance.file)
        instance.photo_type = validated_data.get('photo_type', instance.photo_type)
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.event = validated_data.get('event', instance.event)
        instance.save()

        return instance


class PhotoSerializer(serializers.ModelSerializer):

    event = EventSerializer()

    class Meta:
        model = Photo
        fields = ("year", "id", "title", "photo_type", "file", "last_update", "event")


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = ("id", "name", "description", "website", "level", "ad_image",)
