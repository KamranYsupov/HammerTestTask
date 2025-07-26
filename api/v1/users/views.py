import loguru
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from api.v1.users.serializers import (
    PhoneSerializer,
    CodeSerializer,
    UserProfileSerializer,
    ActivateInviteSerializer, AuthUserSerializer, TokenRefreshSerializer,
)
from users.tasks import send_auth_code
from users.utils import verify_auth_code

User = get_user_model()


class RequestPhoneView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        send_auth_code.delay(phone_number)
        return Response(
            {'detail': 'Код отправлен'},
            status=status.HTTP_200_OK
        )

class VerifyCodeView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        if not verify_auth_code(phone_number, code):
            return Response(
                {'detail': 'Неверный код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone_number=phone_number
            )

        refresh = RefreshToken.for_user(user)

        response_serializer = AuthUserSerializer(
            data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'invite_code': user.invite_code,
                'activated_invite_code': user.activated_invite_code,
            }
        )
        response_serializer.is_valid()

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateInviteCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ActivateInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data['invite_code']
        user = request.user

        if user.activated_invite_code:
            return Response(
                {
                    'detail': f'Вы уже активировали '
                    f'промокод {user.activated_invite_code}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            inviter = User.objects.get(invite_code=invite_code)
            if inviter == user:
                return Response(
                    {
                        'detail': 'Нельзя активировать '
                        'собственный промокод'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {'detail': 'Промокод не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user.invited_by = inviter
            user.activated_invite_code = invite_code
            user.save()

        return Response({'detail': 'Промокод активирован'})


class TokenRefreshView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
        except TokenError as e:
            return Response(
                {'detail': 'Неверный или просроченный refresh токен'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response_serializer = AuthUserSerializer(
            data={
                'access': str(new_access),
                'refresh': str(refresh),
            }
        )
        response_serializer.is_valid()

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
