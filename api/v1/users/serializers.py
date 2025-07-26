from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PhoneNumberSerializerMixin(serializers.Serializer):
    phone_number = serializers.CharField()


class InviteCodeField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_length = kwargs.pop('max_length', 6)


class PhoneSerializer(PhoneNumberSerializerMixin):
    pass


class CodeSerializer(PhoneNumberSerializerMixin):
    code = serializers.CharField()


class ActivateInviteSerializer(serializers.Serializer):
    invite_code = InviteCodeField()


class AuthUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    invite_code = InviteCodeField(
        allow_blank=True,
    )
    activated_invite_code = InviteCodeField(
        default=None,
        allow_null=True,
        allow_blank=True,
    )


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


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
