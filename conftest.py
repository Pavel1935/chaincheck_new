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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def tokens():
    login_url = Constants.API_URL + "/auth/login"

    payload = {
        "email": Constants.EMAIL, "recaptcha_token": "SpartakChampion"
    }

    login_response = requests.post(login_url, json=payload)
    login_response.raise_for_status()
    print("[LOGIN] RESPONSE:", login_response.text)

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

    # return {
    #     "access_token": access_token,
    #     "refresh_token": refresh_token
    # }
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
                    json={}                    )


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


@pytest.fixture(scope="session")
def verification_code_fixture():
    code = get_verification_code()
    print(f"[Fixture] Verification code: {code}")
    return code


def _configure_logging():
    # уровень берём из переменной окружения, по умолчанию INFO
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    # чтобы requests не шумел
    logging.getLogger("urllib3").setLevel(logging.WARNING)

_configured = False


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global _configured
    if not _configured:
        _configure_logging()
        _configured = True


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

@pytest.fixture
def verification_code_redis():
    def _get(email: str) -> str:
        return get_verification_code(email=email)
    return _get

@pytest.fixture
def mock_auth(login_page, tokens):
    """
    Мок авторизации для UI:
    - перехватывает /auth/login и /auth/verify-email
    - возвращает валидные токены из фикстуры tokens
    - логирует запросы и ответы
    """
    page = login_page.page

    LOGIN_URL_PATTERN = "**/auth/login"
    VERIFY_URL_PATTERN = "**/auth/verify-email"

    def login_handler(route, request):
        try:
            payload = request.post_data_json
            email = payload.get("email")
            recaptcha = payload.get("recaptcha_token")
            logger.info(f"[MOCK LOGIN] email={email}, recaptcha={recaptcha}")
        except Exception as e:
            logger.warning(f"[MOCK LOGIN] не удалось распарсить тело запроса: {e}")

        # Возвращаем тот же ответ, что даёт реальный бекенд
        body = {"ok": 1}
        logger.info(f"[MOCK LOGIN RESPONSE] {body}")
        route.fulfill(
            status=200,
            headers={"content-type": "application/json"},
            body=json.dumps(body)
        )

    def verify_handler(route, request):
        try:
            payload = request.post_data_json
            email = payload.get("email")
            code = payload.get("code")
            logger.info(f"[MOCK VERIFY] email={email}, code={code}")
        except Exception as e:
            logger.warning(f"[MOCK VERIFY] не удалось распарсить тело запроса: {e}")

        body = {
            "ok": 1,
            "access-token": tokens["access_token"]
        }
        headers = {
            "content-type": "application/json",
            "set-cookie": f"refresh_token={tokens['refresh_token']}; Path=/; HttpOnly; Secure; SameSite=Lax"
        }
        logger.info(f"[MOCK VERIFY RESPONSE] {body}, headers={headers}")
        route.fulfill(status=200, headers=headers, body=json.dumps(body))

    # Вешаем роуты
    page.route(LOGIN_URL_PATTERN, login_handler)
    page.route(VERIFY_URL_PATTERN, verify_handler)

    yield

    # После теста снимаем, чтобы не протекли в другие
    page.unroute(LOGIN_URL_PATTERN)
    page.unroute(VERIFY_URL_PATTERN)
