import pytest
import requests
from Constants import Constants
import time
from redis_utils import get_verification_code



@pytest.fixture
def access_token():
    endpoint = "/auth/refresh-token"

    url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"

    payload = ""
    headers = {
        'Cookie': 'refresh_token=01985bec-64b6-72ea-9c88-344a7ca3fcc2'
    }

    response = requests.post(url, headers=headers, data=payload)

    token_data = response.json()

    assert "access-token" in token_data, "access-token не найден в ответе"

    print("ACCESS TOKEN:", token_data["access-token"])
    return token_data["access-token"]


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

    return data["result"]["report_id"]  # 💡 вернёт report_id из ответа



# @pytest.fixture(scope="session")
# def verification_code():
#     code = get_verification_code()
#     print(f"[Fixture] Verification code: {code}")
#     return code

@pytest.fixture(scope="session")
def tokens():
    login_url = Constants.API_URL + "/auth/login"

    payload = {
        "email": Constants.EMAIL
    }

    login_response = requests.post(login_url, json=payload)
    login_response.raise_for_status()
    print("[LOGIN] RESPONSE:", login_response.text)

    # 🔽 КОД ПОЛУЧАЕМ ТЕПЕРЬ — ПОСЛЕ login
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
