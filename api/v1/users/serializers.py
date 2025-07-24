from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PhoneNumberSerializerMixin:
    phone_number = serializers.CharField()


class PhoneSerializer(serializers.Serializer, PhoneNumberSerializerMixin):
    pass


class CodeSerializer(serializers.Serializer, PhoneNumberSerializerMixin):
    code = serializers.CharField()

class ActivateInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

class UserProfileSerializer(serializers.ModelSerializer):
    activated_invite_code = serializers.CharField(allow_null=True)
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'phone_number',
            'invite_code',
            'activated_invite_code',
            'invited_users'
        ]

    def get_invited_users(self, obj):
        return obj.invited_users.all().values_list(
            'phone_number',
            flat=True
        )
