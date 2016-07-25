from .models import RegistrationGroup, Registration, SignupSlot
from rest_framework import serializers


class RegistrationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationGroup
        fields = ("id", "event", "course_setup", "signed_up_by", "starting_hole", "starting_order", "notes",
                  "payment_confirmation_code", "payment_confirmation_timestamp", "payment_amount", )


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ("id", "registration_group", "member", "is_event_fee_paid", "is_greens_fee_paid",
                  "is_gross_skins_paid", "is_net_skins_paid", )


class SignupSlotSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source="course_setup_hole.course_setup.name")
    course_setup_id = serializers.CharField(source="course_setup_hole.course_setup.id")
    hole = serializers.IntegerField(source="course_setup_hole.hole_number")
    member_first_name = serializers.CharField(source="member.first_name")
    member_last_name = serializers.CharField(source="member.last_name")

    class Meta:
        model = SignupSlot
        fields = ("id", "course", "course_setup_id", "hole", "registration_group",
                  "member", "member_first_name", "member_last_name",
                  "starting_order", "slot", "status", "expires")
