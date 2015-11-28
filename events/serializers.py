from .models import Event, EventTemplate
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ("url", "id", "name", "courses", "description", "start_date", "rounds", "holes_per_round",
                  "signup_start", "signup_end", "start_time", "event_fee", "skins_fee", "minimum_signup_group_size",
                  "maximum_signup_group_size", "group_size", "is_shotgun_start", "can_signup_group", "can_choose_hole",
                  "scoring", "scoring_system", "team_scoring", "number_of_scores")


class EventTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventTemplate
        fields = ("url", "id", "name", "description", "rounds", "holes_per_round", "event_fee", "skins_fee",
                  "minimum_signup_group_size", "maximum_signup_group_size", "group_size", "is_shotgun_start",
                  "can_signup_group", "can_choose_hole", "scoring", "scoring_system", "team_scoring",
                  "number_of_scores")
