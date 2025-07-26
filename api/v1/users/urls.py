from django.urls import path
from api.v1.users.views import (
    RequestPhoneView,
    VerifyCodeView,
    ProfileView,
    ActivateInviteCodeView,
    TokenRefreshView,
)

urlpatterns = [
    path('request-code/', RequestPhoneView.as_view(), name='request-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path(
        'profile/activate-invite/',
        ActivateInviteCodeView.as_view(),
        name='activate-invite'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
