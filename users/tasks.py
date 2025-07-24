import time

import loguru
from django.core.cache import cache
from django.conf import settings

from .utils import generate_code
from core.celery import app

@app.task()
def send_code(phone_number):
    """Задача для отправки кода на телефон"""
    code = generate_code(length=4, use_letters=False)
    cache.set(f'auth_code_{phone_number}', code, settings.AUTH_CODE_TTL)

    time.sleep(2)
    loguru.logger.info(f'Отправлен код {code} на номер {phone_number}') # Имитация отправки SMS