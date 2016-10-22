from django.contrib.auth.models import User
from .models import Club, Member
from rest_framework import serializers


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ("url", "id", "description", "address1", "address2", "city", "state",
                  "zip", "website", "contact_email", "phone_number")


class MemberDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ("id", "address1", "address2", "city", "state", "zip",
                  "phone_number", "handicap", "handicap_revision_date",
                  "birth_date", "status", "summary", "payment_method",
                  "stripe_customer_id", "stripe_save_card")


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    member = MemberDetailSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "member",
                  "is_authenticated", "is_staff", "is_active")
        read_only_fields = ("id", "is_authenticated", "is_staff", "is_active")

    def update(self, instance, validated_data):
        member_data = validated_data.pop('member')
        member = instance.member

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        member.address1 = member_data.get('address1', member.address1)
        member.address2 = member_data.get('address2', member.address2)
        member.city = member_data.get('city', member.city)
        member.state = member_data.get('state', member.state)
        member.zip = member_data.get('zip', member.zip)
        member.phone_number = member_data.get('phone_number', member.phone_number)
        member.handicap = member_data.get('handicap', member.handicap)
        member.handicap_revision_date = member_data.get('handicap_revision_date', member.handicap_revision_date)
        member.birth_date = member_data.get('birth_date', member.birth_date)
        member.status = member_data.get('status', member.status)
        member.summary = member_data.get('summary', member.summary)
        member.payment_method = member_data.get('payment_method', member.payment_method)
        member.stripe_customer_id = member_data.get('stripe_customer_id', member.stripe_customer_id)
        member.stripe_save_card = member_data.get('stripe_save_card', member.stripe_save_card)
        member.save()

        return instance


# All public information
class MemberSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    user_id = serializers.CharField(source="user.id")

    class Meta:
        model = Member
        fields = ("url", "first_name", "last_name", "email",
                  "address1", "address2", "city", "state", "zip",
                  "phone_number", "handicap", "handicap_revision_date",
                  "user_id", "birth_date", "status", "summary",
                  "thumbnail_url", "profile_url")
