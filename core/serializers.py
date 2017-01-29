from django.contrib.auth.models import User, Group
from .models import Club, Member, SeasonSettings
from rest_framework import serializers


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ("url", "id", "description", "address1", "address2", "city", "state",
                  "zip", "website", "contact_email", "phone_number")


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeasonSettings
        fields = ('year', 'reg_event', 'match_play_event', 'accept_new_members', 'website_version', 'api_version',
                  'raven_dsn', 'stripe_pk', )


class MemberDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ("id", "address1", "address2", "city", "state", "zip",
                  "phone_number", "handicap", "handicap_revision_date", "ghin",
                  "birth_date", "status", "summary", "stripe_customer_id", "forward_tees",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    member = MemberDetailSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "member",
                  "is_authenticated", "is_staff", "is_active", "password", "groups", )
        read_only_fields = ("id", "is_authenticated", "is_staff", "is_active", )

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
        member.save()

        return instance

    def create(self, validated_data):
        member_data = validated_data.pop('member')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        Member.objects.create(
            address1=member_data.get('address1', ''),
            city=member_data.get('city', ''),
            zip=member_data.get('zip', ''),
            phone_number=member_data['phone_number'],
            birth_date=member_data['birth_date'],
            ghin=member_data.get('ghin', ''),
            forward_tees=member_data.get('forward_tees', False),
            user=user
        )
        return user


class SimpleMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Member
        fields = ("id", "first_name", "last_name", "email", )


# All public information
class MemberSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    user_id = serializers.CharField(source="user.id")

    class Meta:
        model = Member
        fields = ("id", "first_name", "last_name", "email",
                  "address1", "address2", "city", "state", "zip",
                  "phone_number", "handicap", "handicap_revision_date",
                  "user_id", "birth_date", "status", "summary",
                  "thumbnail_url", "profile_url", "forward_tees")
