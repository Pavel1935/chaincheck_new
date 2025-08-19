import requests
from Constants import Constants
import time
from redis_utils import get_verification_code
import logging
import os
import pytest


@pytest.fixture(scope="session")
def tokens():
    login_url = Constants.API_URL + "/auth/login"

    payload = {
        "email": Constants.EMAIL
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

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


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
        "wallet": "bc1q29k0jkvpekcuv6dwchjww8pev92gsxe9uw24wz",
        "network": "btc"
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