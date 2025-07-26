import loguru
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.text import gettext_lazy as _
from django.db import models

from users.utils import generate_unique_invite_code


class UserManager(BaseUserManager):
    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.invite_code = generate_unique_invite_code()
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        _('Номер телефона'),
        max_length=20,
        unique=True
    )
    invite_code = models.CharField(
        _('Код приглашения'),
        max_length=6,
        unique=True
    )
    activated_invite_code = models.CharField(
        _('Активированный код приглашения'),
        max_length=6,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        _('Активный'),
        default=True
    )
    is_staff = models.BooleanField(
        _('Статус персонала'),
        default=False
    )

    invited_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='invited_users',
        verbose_name=_('Приглашен пользователем')
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

