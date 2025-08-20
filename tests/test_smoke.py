import pytest
import requests
import time
from Constants import Constants
from conftest import wait_for_report_ready
import allure
from redis_utils import get_verification_code
from loguru import logger
from conftest import login_page


class TestCheckSmoke:
    @pytest.mark.smoke
    @allure.step('Проверка адреса в сети BTC')
    def test_check_smoke_btc_ok(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
            "network": "btc"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        report_id_smoke = data["result"]["report_id"]

        data = wait_for_report_ready(report_id_smoke, headers, Constants.API_URL)
        assert data["ok"] == 1

        url_check = Constants.API_URL + "/aml/check/history/one"
        response = requests.post(url_check, headers=headers, json={"report_id": report_id_smoke})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.smoke
    @allure.step('Проверка адреса в сети BSC')
    def test_check_smoke_bsc_ok(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
            "network": "bsc"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)
        data = response.json()
        assert data["ok"] == 1
        report_id_smoke = data["result"]["report_id"]

        data = wait_for_report_ready(report_id_smoke, headers, Constants.API_URL)
        assert data["ok"] == 1

        url_check = Constants.API_URL + "/aml/check/history/one"
        response = requests.post(url_check, headers=headers, json={"report_id": report_id_smoke})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.smoke
    @allure.step('Проверка адреса в сети ETH')
    def test_check_smoke_ether_ok(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0xc8Bd2FBFe0437f38394C5d504221FC01CC8dF92a",
            "network": "ether"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)
        data = response.json()
        assert data["ok"] == 1
        report_id_smoke = data["result"]["report_id"]

        data = wait_for_report_ready(report_id_smoke, headers, Constants.API_URL)
        assert data["ok"] == 1

        url_check = Constants.API_URL + "/aml/check/history/one"
        response = requests.post(url_check, headers=headers, json={"report_id": report_id_smoke})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.smoke
    @allure.step('Проверка адреса в сети TRON')
    def test_check_smoke_tron_ok(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "TK9YEyYQS9H66S53eT78N2YnVpDmAy3qTV",
            "network": "tron"
        }

        access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        report_id_smoke = data["result"]["report_id"]

        data = wait_for_report_ready(report_id_smoke, headers, Constants.API_URL)
        assert data["ok"] == 1

        url_check = Constants.API_URL + "/aml/check/history/one"
        response = requests.post(url_check, headers=headers, json={"report_id": report_id_smoke})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.smoke
    @allure.step('Негативная проверка неверного report_id')
    def test_smoke_negative_api_incorrect_report_id(self, tokens):
        access_token = tokens["access_token"]
        headers = {'Authorization': 'Bearer ' + access_token}

        url_check = Constants.API_URL + "aml/check"
        payload = {
            "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
            "network": "btc"
        }

        response = requests.post(url_check, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)
        data = response.json()
        assert data["ok"] == 1
        report_id = 123

        time.sleep(1)

        url_history = Constants.API_URL + "/aml/check/history/one"
        response = requests.post(url_history, headers=headers, json={"report_id": report_id})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    @pytest.mark.smoke
    @allure.step('Негативная проверка протухшего токена авторизации')
    def test_smoke_negative_api_old_access_token(self, tokens):
        access_token = tokens["access_token"]
        headers_1 = {'Authorization': 'Bearer ' + access_token}

        url_check = Constants.API_URL + "aml/check"
        payload = {
            "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
            "network": "bsc"
        }

        response = requests.post(url_check, headers=headers_1, json=payload)
        data = response.json()
        assert data["ok"] == 1
        report_id_smoke = data["result"]["report_id"]

        time.sleep(1)

        url_history = Constants.API_URL + "/aml/check/history/one"
        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyMjE3NzUyLCJuYmYiOjE3NTIxMzEzNTIsImlhdCI6MTc1MjEzMTM1MiwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.T6qR_3EkMX4_1uBDdV8vM7GXqfbZzcaakDRuxxkgiAU"}
        response = requests.post(url_history, headers=headers,
                                 json={"report_id": report_id_smoke})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    class TestLoginFlow:
        @pytest.mark.smoke
        @allure.step('Позитивная проверка входа по email')
        def test_email_login_ui(self, login_page):
            logger.info("Начинаю тест: вход по email")

            login_page.open("https://check-dev.g5dl.com")

            login_page.enter_wallet_address("0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f")
            login_page.enter_email(Constants.EMAIL)

            code = get_verification_code()
            login_page.enter_code(code)

            login_page.check_final_result()
            logger.info("Проверили результат")


