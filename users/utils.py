import random
import secrets
import string

import loguru
from django.contrib.auth import get_user_model
from django.core.cache import cache


def generate_code(
        length: int = 6,
        use_letters: bool = True,
) -> str:
    """Генерирует случайный код"""
    chars = string.digits
    chars += string.ascii_letters if use_letters else ''

    return ''.join(random.choices(chars, k=length))


def generate_unique_invite_code(length: int = 6) -> str:
    """Генерирует уникальный случайный код приглашения"""
    invite_code = generate_code(length=length)
    invite_code_exists = get_user_model().objects.filter(invite_code=invite_code).exists()
    while invite_code_exists:
        invite_code = generate_code(length=length)
        invite_code_exists = get_user_model().objects.filter(invite_code=invite_code).exists()


    return invite_code


def verify_auth_code(phone_number: str | int, code: str) -> bool:
    key = f'auth_code_{phone_number}'
    cached_code = cache.get(key)

    return False if not cached_code \
        else secrets.compare_digest(cached_code, code)
