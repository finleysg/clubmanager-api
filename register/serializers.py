from rest_framework import serializers

from core.models import Member
from core.serializers import SimpleMemberSerializer
from .models import RegistrationGroup, RegistrationSlot, RegistrationSlotPayment


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
        order_by = ("hole_number", "starting_order", )

    def update(self, instance, validated_data):
        member = instance.member
        if member is None:
            member_data = validated_data.pop('member')
            member = Member.objects.get(pk=member_data['id'])

        instance.member = member
        instance.registration_group = validated_data.get('registration_group', instance.registration_group)
        instance.is_event_fee_paid = validated_data.get('is_event_fee_paid', instance.is_event_fee_paid)
        instance.is_net_skins_paid = validated_data.get('is_net_skins_paid', instance.is_net_skins_paid)
        instance.is_gross_skins_paid = validated_data.get('is_gross_skins_paid', instance.is_gross_skins_paid)
        instance.is_greens_fee_paid = validated_data.get('is_greens_fee_paid', instance.is_greens_fee_paid)
        instance.is_cart_fee_paid = validated_data.get('is_cart_fee_paid', instance.is_cart_fee_paid)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance


class RegistrationGroupSerializer(serializers.ModelSerializer):

    signed_up_by = SimpleMemberSerializer()
    slots = RegistrationSlotSerializer(many=True)

    class Meta:
        model = RegistrationGroup
        fields = ("id", "event", "course_setup", "signed_up_by", "starting_hole", "starting_order", "notes",
                  "payment_confirmation_code", "payment_confirmation_timestamp", "payment_amount",
                  "card_verification_token", "slots", "expires")


class RegistrationSlotPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrationSlotPayment
        fields = ("id", "registration_slot", "recorded_by", "card_verification_token",
                  "payment_code", "payment_timestamp", "payment_amount", "comment")
