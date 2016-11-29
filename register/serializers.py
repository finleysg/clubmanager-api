from rest_framework import serializers
from .models import RegistrationGroup, RegistrationSlot


class RegistrationSlotSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source="course_setup_hole.course_setup.name")
    course_setup_id = serializers.CharField(source="course_setup_hole.course_setup.id")
    hole = serializers.IntegerField(source="course_setup_hole.hole_number")
    member_first_name = serializers.CharField(source="member.user.first_name")
    member_last_name = serializers.CharField(source="member.user.last_name")

    class Meta:
        model = RegistrationSlot
        fields = ("id", "course", "course_setup_id", "hole", "registration_group",
                  "member", "member_first_name", "member_last_name",
                  "is_event_fee_paid", "is_greens_fee_paid", "is_gross_skins_paid", "is_net_skins_paid",
                  "starting_order", "slot", "status", "expires")


class RegistrationGroupSerializer(serializers.ModelSerializer):

    slots = RegistrationSlotSerializer(many=True)

    class Meta:
        model = RegistrationGroup
        fields = ("id", "event", "course_setup", "signed_up_by", "starting_hole", "starting_order", "notes",
                  "payment_confirmation_code", "payment_confirmation_timestamp", "payment_amount", "slots")
