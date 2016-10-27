from .models import Event, EventTemplate
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ("url", "id", "name", "description", "rounds", "holes_per_round", "event_fee", "skins_fee",
                  "minimum_signup_group_size", "maximum_signup_group_size", "group_size", "start_type",
                  "can_signup_group", "can_choose_hole", "scoring", "scoring_system", "event_state", "external_url",
                  "number_of_scores", "notes", "event_type", "skins_type", "season_points", "requires_registration",
                  "template", "start_date", "start_time", "end_date", "end_time", "signup_start", "signup_end",
                  "registration_maximum", "course_setups")


class EventTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventTemplate
        fields = ("url", "id", "name", "description", "rounds", "holes_per_round", "event_fee", "skins_fee",
                  "minimum_signup_group_size", "maximum_signup_group_size", "group_size", "start_type",
                  "can_signup_group", "can_choose_hole", "scoring", "scoring_system", "external_url",
                  "number_of_scores", "notes", "event_type", "skins_type", "season_points", "requires_registration",)
