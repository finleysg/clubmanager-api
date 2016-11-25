from .models import Event, EventTemplate
from documents.models import Document
from rest_framework import serializers


class EventDocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ("url", "id", "title", "document_type", "file", )


class EventSerializer(serializers.HyperlinkedModelSerializer):

    documents = EventDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ("url", "id", "name", "description", "rounds", "holes_per_round", "event_fee", "skins_fee",
                  "minimum_signup_group_size", "maximum_signup_group_size", "group_size", "start_type",
                  "can_signup_group", "can_choose_hole", "registration_window", "external_url",
                  "notes", "event_type", "skins_type", "season_points", "requires_registration",
                  "template", "start_date", "start_time", "enable_payments", "signup_start", "signup_end",
                  "registration_maximum", "course_setups", "documents", )


class EventTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventTemplate
        fields = ("url", "id", "name", "description", "rounds", "holes_per_round", "event_fee", "skins_fee",
                  "minimum_signup_group_size", "maximum_signup_group_size", "group_size", "start_type",
                  "can_signup_group", "can_choose_hole", "external_url",
                  "notes", "event_type", "skins_type", "season_points", "requires_registration", )
