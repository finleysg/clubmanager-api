from django.contrib.auth.models import User
from .models import Club, Member
from rest_framework import serializers


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ("url", "id", "description", "address1", "address2", "city", "state",
                  "zip", "website", "contact_email", "phone_number")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "first_name", "last_name", "email")


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    user_id = serializers.CharField(source="user.id")

    class Meta:
        model = Member
        fields = ("url", "first_name", "last_name", "email",
                  "address1", "address2", "city", "state", "zip",
                  "ghin", "phone_number", "handicap", "handicap_revision_date",
                  "user_id", "show_phone", "show_email")
