from .models import SignupGroup, Signup, SignupSlot
from rest_framework import serializers


class SignupGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SignupGroup
        fields = ("url", "id", "event", "course_setup", "starting_hole", "starting_order", "start_time")


class SignupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Signup
        fields = ("url", "id", "signup_group", "member", "is_event_fee_paid", "is_greens_fee_paid",
                  "is_gross_skins_paid", "is_net_skins_paid", "signed_up_by")


class SignupSlotSerializer(serializers.HyperlinkedModelSerializer):
    event_name = serializers.CharField(source="event.name")
    event_date = serializers.DateField(source="event.start_date")
    course = serializers.CharField(source="course_setup_hole.course_setup.name")
    hole = serializers.IntegerField(source="course_setup_hole.hole_number")
    member_first_name = serializers.CharField(source="member.first_name")
    member_last_name = serializers.CharField(source="member.last_name")

    class Meta:
        model = SignupSlot
        fields = ("url", "id", "event", "event_name", "event_date",
                  "course_setup_hole", "course", "hole",
                  "member", "member_first_name", "member_last_name",
                  "starting_order", "slot", "status", "expires")