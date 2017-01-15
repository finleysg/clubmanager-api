from rest_framework import serializers

from core.serializers import MemberSerializer, SimpleMemberSerializer
from .models import RegistrationGroup, RegistrationSlot


# class RegisteredMemberSerializer(serializers.ModelSerializer):
#
#     member = MemberSerializer()
#
#     class Meta:
#         model = RegistrationSlot
#         fields = ("member", )


class RegistrationSlotSerializer(serializers.ModelSerializer):
    member = SimpleMemberSerializer()
    course = serializers.CharField(source="course_setup_hole.course_setup.name")
    course_setup_id = serializers.CharField(source="course_setup_hole.course_setup.id")
    hole_number = serializers.IntegerField(source="course_setup_hole.hole_number")
    hole_id = serializers.IntegerField(source="course_setup_hole.id")

    class Meta:
        model = RegistrationSlot
        fields = ("id", "event", "course", "course_setup_id", "hole_number", "hole_id", "registration_group",
                  "is_event_fee_paid", "is_greens_fee_paid", "is_gross_skins_paid", "is_net_skins_paid",
                  "is_cart_fee_paid", "starting_order", "slot", "status", "member")


class RegistrationGroupSerializer(serializers.ModelSerializer):

    slots = RegistrationSlotSerializer(many=True)

    class Meta:
        model = RegistrationGroup
        fields = ("id", "event", "course_setup", "signed_up_by", "starting_hole", "starting_order", "notes",
                  "payment_confirmation_code", "payment_confirmation_timestamp", "payment_amount",
                  "card_verification_token", "slots", "expires")
