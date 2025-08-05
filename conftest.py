import pytest
import requests
from Constants import Constants
import time
from redis_utils import get_verification_code



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

@pytest.fixture(scope="session")
def refresh_token():
    login_url = Constants.API_URL + "/auth/login"

    payload = {
        "email": Constants.EMAIL
    }

    login_response = requests.post(login_url, json=payload)
    login_response.raise_for_status()
    # print("[LOGIN] RESPONSE:", login_response.text)


    from redis_utils import get_verification_code
    code = get_verification_code()
    # print(f"[Verification code] Received: {code}")

    # verify
    verify_url = Constants.API_URL + "/auth/verify-email"
    body = {
        "email": Constants.EMAIL,
        "code": code
    }

    verify_response = requests.post(verify_url, json=body)
    verify_response.raise_for_status()
    # print("[VERIFY] RESPONSE:", verify_response.text)

    data = verify_response.json()
    assert data.get("ok") == 1, f"Verify failed: {data}"

     # access_token = data.get("access-token")
    refresh_token = verify_response.cookies.get("refresh_token")

    # print(f"[TOKENS] Access: {access_token}")
    print(f"[TOKENS] Refresh: {refresh_token}")

    return refresh_token


@pytest.fixture(scope="session")
def access_token_only(tokens):
    return tokens["access_token"]

@pytest.fixture
def get_access_token(refresh_token):
    url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"

    payload = ""
    headers = {
        'Cookie': f'refresh_token={refresh_token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    print("RESPONSE TEXT:", response.text)

    data = response.json()

    return data["access-token"]


@pytest.fixture
def report_id():

    url = Constants.API_URL + "aml/check"

    payload = {
        "wallet": "0x1234567890abcdef1234567890abcdef12345678",
        "network": "bsc"
    }
    headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

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


