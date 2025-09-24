import os

import pytest
import redis
import time

REDIS_KEY = "ea:oukb1147@gmail.com"


def get_redis_connection():
    return redis.Redis(
        host="167.235.223.2",
        port=57379,
        password="teuneedap3ju",
        db=0,
        decode_responses=True
    )


def get_verification_code(email=None, retries=None, delay=None) -> str:
    """Пытается получить код подтверждения из Redis с повторными попытками"""
    redis_conn = get_redis_connection()

    retries = retries or int(os.getenv("REDIS_RETRIES", "30"))  # по умолчанию ждём до 30 секунд
    delay = delay or int(os.getenv("REDIS_DELAY", "1"))

    for attempt in range(retries):
        code = redis_conn.get(REDIS_KEY if email is None else f"ea:{email}")
        if code:
            print(f"[Redis] Код из Redis: {code}")
            return code
        time.sleep(delay)

    pytest.fail(f"Код не найден в Redis по ключу {REDIS_KEY} после {retries*delay} секунд")


