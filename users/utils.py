import random
import string

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
    invite_code = generate_code()
    invite_code_exists = get_user_model().objects.filter(invite_code=invite_code).exists()
    while invite_code_exists:
        invite_code = generate_code()
        invite_code_exists = get_user_model().objects.filter(invite_code=invite_code).exists()

    return invite_code


def verify_auth_code(phone_number, code):
    cached_code = cache.get(f"auth_code_{phone_number}")
    return cached_code == code
