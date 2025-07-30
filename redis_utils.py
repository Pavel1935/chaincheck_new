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


def get_verification_code(retries=10, delay=1) -> str:
    """Пытается получить код подтверждения из Redis с повторными попытками"""
    redis_conn = get_redis_connection()

    for attempt in range(retries):
        code = redis_conn.get(REDIS_KEY)
        if code:
            print(f"[Redis] Код из Redis: {code}")
            return code
        time.sleep(delay)

    raise TimeoutError(f"Код не найден в Redis по ключу {REDIS_KEY} после {retries} попыток")
