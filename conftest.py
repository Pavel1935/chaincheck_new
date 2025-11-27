import requests
from Constants import Constants
import time
from redis_utils import get_verification_code
import logging
import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from contextlib import suppress
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import pytest
from pathlib import Path
from telethon.sync import TelegramClient

# Файл сессии лежит рядом с тестами (например tests/chainscheck_qa_bot.session)
SESSION_PATH = str(Path(__file__).parent / "chainscheck_qa_bot.session")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
_TOKENS_CACHE = None  # защита от повторного логина

"""ФИКСТУРА КОТОРАЯ ИСПОЛЬЗУЕТСЯ ВО ВСЕХ ТЕСТАХ, ГДЕ СОХРАНЯЕТ ДАННЫЕ В ОДНОЙ
СЕССИИ И НЕ ИСПОЛЬЗУЕТ НОВЫЕ ЛОГИНЫ ДЛЯ ПОСЛЕДУЮЩИХ ТЕСТОВ!!! """
@pytest.fixture(scope="session")
def class_tokens():
    """
    1 раз за сессию логинимся по API и возвращаем токены.
    Никаких повторных обращений к /auth/login.
    """
    global _TOKENS_CACHE
    if _TOKENS_CACHE:
        logger.info("[TOKENS] Использую кэшированный токен")
        return _TOKENS_CACHE

    logger.info("[TOKENS] Выполняю логин для всей сессии")
    login_url = f"{Constants.API_URL}/auth/login"
    payload = {"email": Constants.EMAIL,
               "recaptcha_token": "SpartakChampion",
               "recaptcha_version": "v2"
               }

    login_response = requests.post(login_url, json=payload)
    login_response.raise_for_status()
    data = login_response.json()
    if not data.get("ok"):
        pytest.fail(f"Login failed for {Constants.EMAIL}: {data}")

    # получаем код из Redis и подтверждаем
    code = get_verification_code()
    verify_url = f"{Constants.API_URL}/auth/verify-email"
    body = {"email": Constants.EMAIL, "code": code}
    verify_response = requests.post(verify_url, json=body)
    verify_response.raise_for_status()
    data = verify_response.json()
    assert data.get("ok") == 1, f"Verify failed: {data}"

    access_token = data.get("access-token")
    refresh_token = verify_response.cookies.get("refresh_token")
    assert refresh_token, "refresh_token отсутствует в cookies verify_response"

    _TOKENS_CACHE = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return _TOKENS_CACHE

"""ФИКСТУРА С НОВОЙ АВТОРИЗАЦИЕЙ, КОГДА НУЖЕН НОВЫЙ ТОКЕН ВХОДА КАЖДЫЙ РАЗ!!!!"""
@pytest.fixture(scope="function")
def tokens():
    login_url = Constants.API_URL + "/auth/login"
    payload = {"email": Constants.EMAIL,
               "recaptcha_token": "SpartakChampion",
               "recaptcha_version": "v2"
               }

    login_response = requests.post(login_url, json=payload)
    login_response.raise_for_status()
    data = login_response.json()
    print("[LOGIN] RESPONSE:", data)

    if not data.get("ok"):
        pytest.fail(f"Login failed for {Constants.EMAIL}: {data}")

    from redis_utils import get_verification_code
    code = get_verification_code()
    print(f"[Verification code] Received: {code}")

    # verify
    verify_url = Constants.API_URL + "/auth/verify-email"
    body = {
        "email": Constants.EMAIL,
        "code": code
    }

    verify_response = requests.post(verify_url, json=body)
    verify_response.raise_for_status()
    print("[VERIFY] RESPONSE:", verify_response.text)

    data = verify_response.json()
    assert data.get("ok") == 1, f"Verify failed: {data}"

    access_token = data.get("access-token")
    refresh_token = verify_response.cookies.get("refresh_token")
    print(f"[TOKENS] Access: {access_token}")
    print(f"[TOKENS] Refresh: {refresh_token}")

    creds = {
                "access_token": data.get("access-token"),
                "refresh_token": verify_response.cookies.get("refresh_token")
                }
    yield creds
    #logout
    with suppress(Exception):
                 requests.get(
                    f"{Constants.API_URL}/logout",
                    headers={"Authorization": f"Bearer {creds['access_token']}"},
                    cookies={"refresh_token": creds["refresh_token"]},
                    json={}
                 )

"""ФИКСТУРА ПАРАМЕТРИЗОВАННАЯ С НОВОЙ АВТОРИЗАЦИЕЙ ДЛЯ КАЖДОЙ РОЛИ(EMAIL),
# КОГДА НУЖЕН НОВЫЙ ТОКЕН ВХОДА КАЖДЫЙ РАЗ КАК ДЛЯ ПАРАМЕТРИЗАЦИИ ТАК И НЕТ!!!!"""
@pytest.fixture(scope="function")
def email(request):
    def _login(email):
        login_url = f"{Constants.API_URL}/auth/login"
        payload = {
            "email": email,
            "recaptcha_token": "SpartakChampion",
            "recaptcha_version": "v2",
        }

        login_response = requests.post(login_url, json=payload)
        login_response.raise_for_status()
        data = login_response.json()

        code = get_verification_code(email=email)

        verify_url = f"{Constants.API_URL}/auth/verify-email"
        verify_payload = {"email": email, "code": code}
        verify_response = requests.post(verify_url, json=verify_payload)
        verify_data = verify_response.json()

        return {
            "email": email,
            "access_token": verify_data.get("access-token"),
            "refresh_token": verify_response.cookies.get("refresh_token"),
        }

    return _login(request.param)


"""ФИКСТУРА ПОЛУЧЕНИЯ ТОКЕНА АВТОРИЗАЦИИ"""
@pytest.fixture
def get_access_token(tokens):
    url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"
    refresh_token = tokens["refresh_token"]

    payload = ""
    headers = {
        'Cookie': f'refresh_token={refresh_token}'
    }

    response = requests.post(url, headers=headers, data=payload)
    print("RESPONSE TEXT:", response.text)

    data = response.json()
    return data["access-token"]


# ФИКСТУРА ПОЛУЧЕНИЯ REPORT_ID
@pytest.fixture
def report_id(tokens):

    url = Constants.API_URL + "aml/check"
    access_token = tokens["access_token"]
    payload = {
        "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
        "network": "bsc"
    }
    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.post(url, headers=headers, json=payload)
    print("RESPONSE TEXT:", response.text)

    data = response.json()
    assert data["ok"] == 1
    time.sleep(1)

    return data["result"]["report_id"]

"""ФИКСТУРА ПОЛУЧЕНИЯ КОДА ВЕРИФИКАЦИИ ИЗ РЕДИС"""
@pytest.fixture(scope="session")
def verification_code_fixture():
    code = get_verification_code()
    print(f"[Fixture] Verification code: {code}")
    return code


"""УТИЛИТА КОТОТАЯ ОЖИДАЕТ ГОТОВНОСТЬ ОТЧЕТА AML В API ТЕСТАХ"""
def wait_for_report_ready(report_id, headers, base_url, timeout=10, interval=0.5):
    """
    Ожидает пока отчет будет готов в течение timeout секунд.

    :param report_id: ID отчета
    :param headers: заголовки (с токеном авторизации)
    :param base_url: базовый URL API
    :param timeout: сколько максимум ждать (в секундах)
    :param interval: как часто опрашивать (в секундах)
    :return: json ответа, когда готов
    :raises TimeoutError: если отчет не готов за timeout
    """
    url_check = base_url + "/aml/check/history/one"
    start = time.time()

    while time.time() - start < timeout:
        response = requests.post(url_check, headers=headers, json={"report_id": report_id})
        data = response.json()
        if data.get("ok") == 1:
            return data
        time.sleep(interval)  # маленькая пауза перед новой попыткой

    raise TimeoutError(f"Report {report_id} was not ready in {timeout} seconds")

"""ФИКСТУРА КОТОРАЯ ЗАПУСКАЕТ UI Playwright и CI"""
@pytest.fixture
def login_page():
    logger.info("Запуск Playwright и браузера")
    # В CI (GitHub Actions переменная CI=true) -> headless
    is_ci = os.getenv("CI", "false").lower() == "true"
    headless = True if is_ci else False
    slow_mo = int(os.getenv("SLOW_MO", "500"))

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            slow_mo=slow_mo
        )
        context = browser.new_context()
        page = context.new_page()
        login_page = LoginPage(page)

        logger.info("Создание объекта LoginPage")
        yield login_page

        logger.info("Закрытие браузера")
        context.close()
        browser.close()

"""ФИКСТУРА ПОЛУЧЕНИЯ ВЕРИФИКАЦИОННОГО КОДА ИЗ РЕДИС"""
@pytest.fixture
def verification_code_redis():
    def _get(email: str) -> str:
        return get_verification_code(email=email)
    return _get

"""ПОДКЛЮЧЕНИЕ К PostgreSQL"""
@pytest.fixture(scope="session")
def db_conn():
    """
    Эта фикстура подключается к базе данных PostgreSQL.
    Она нужна, чтобы мы могли проверить, что у пользователя
    в таблице users действительно стоит нужная роль (role).
    """
    # создаём соединение с базой
    conn = psycopg2.connect(
        dbname="backend",        # название твоей БД
        user="postgres",         # имя пользователя PostgreSQL
        password="aik4eeheifai",     # пароль
        host="167.235.223.2",        # адрес сервера (например localhost или IP)
        port="55432",             # стандартный порт PostgreSQL
    )

    # "yield" означает, что мы отдаём соединение тестам
    yield conn

    # после завершения тестов соединение закрывается
    conn.close()


"""Запрос в базу: получить роль пользователя"""
def get_user_role(conn, email):
    """
    Получает роль пользователя из таблицы users по email.
    Мы делаем SELECT в PostgreSQL напрямую.
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # выполняем SQL-запрос
        cur.execute("SELECT role FROM users WHERE email = %s", (email,))

        # получаем результат в виде словаря: {'role': 1}
        result = cur.fetchone()

        # если пользователь найден — возвращаем его роль
        return result["role"] if result else None


"""ПОДКЛЮЧЕНИЕ К Telegram"""
@pytest.fixture(scope="session")
def telegram_client():
    """
    Один раз авторизуется в Telegram и сохраняет сессию.
    На следующих запусках просто переподключается.
    """
    client = TelegramClient(SESSION_PATH, Constants.API_ID, Constants.API_HASH)
    client.start(phone=Constants.PHONE_NUMBER)  # если сессии нет — запросит код только первый раз
    print("\n[SESSION FIXTURE] Telegram клиент подключён.")
    yield client
    client.disconnect()
    print("[SESSION FIXTURE] Telegram клиент отключён.")


# """ФИКСУТРА КОТОТАЯ МОКИРУЕТ ПОЛУЧЕНИЕ ВЕРИФИКАЦИОННОГО КОДА ИЗ РЕДИС"""
# @pytest.fixture
# def verification_code_redis_moc():
#     def _get(email: str) -> str:
#         return get_verification_code_moc(email=email)
#     return _get


#ФИКСУТРА КОТОТАЯ МОКИРУЕТ АВТОРИЗАЦИЮ
# @pytest.fixture()
# def tokens_moc():
#     login_url = Constants.API_URL + "/auth/login"
#
#     payload = {
#         "email": Constants.MOCK_EMAIL, "recaptcha_token": "SpartakChampion"
#     }
#
#     login_response = requests.post(login_url, json=payload)
#     login_response.raise_for_status()
#     data = login_response.json()
#     print("[LOGIN] RESPONSE:", data)
#
#     if not data.get("ok"):
#         pytest.fail(f"Login failed for {Constants.MOCK_EMAIL}: {data}")
#
#     from redis_utils import get_verification_code_moc
#     code = get_verification_code_moc()
#     print(f"[Verification code] Received: {code}")
#
#     # verify
#     verify_url = Constants.API_URL + "/auth/verify-email"
#     body = {
#         "email": Constants.MOCK_EMAIL,
#         "code": code
#     }
#
#     verify_response = requests.post(verify_url, json=body)
#     verify_response.raise_for_status()
#     print("[VERIFY] RESPONSE:", verify_response.text)
#
#     data = verify_response.json()
#     assert data.get("ok") == 1, f"Verify failed: {data}"
#
#     access_token = data.get("access-token")
#     refresh_token = verify_response.cookies.get("refresh_token")
#     print(f"[TOKENS] Access: {access_token}")
#     print(f"[TOKENS] Refresh: {refresh_token}")
#
#     creds = {
#                 "access_token": data.get("access-token"),
#                 "refresh_token": verify_response.cookies.get("refresh_token")
#                 }
#     yield creds
#     #logout
#     with suppress(Exception):
#                  requests.get(
#                     f"{Constants.API_URL}/logout",
#                     headers={"Authorization": f"Bearer {creds['access_token']}"},
#                     cookies={"refresh_token": creds["refresh_token"]},
#                     json={}
#                  )


#
#
