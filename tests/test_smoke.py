import requests
import time
from conftest import wait_for_report_ready
from loguru import logger
from conftest import login_page
import pytest
import allure
from Constants import Constants
from redis_utils import get_verification_code


@pytest.mark.usefixtures("class_tokens")
class TestCheckSmokeAPI:
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.step('Проверка адреса в сети BTC')
    def test_check_smoke_btc_ok(self, class_tokens):
        logger.info("Начинаю тест: проверка адреса в сети BTC")
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
            "network": "btc"
        }

        access_token = class_tokens["access_token"]

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
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.api
    @allure.step('Проверка адреса в сети BSC')
    def test_check_smoke_bsc_ok(self, class_tokens):
        logger.info("Начинаю тест: проверка адреса в сети BSC")
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
            "network": "bsc"
        }

        access_token = class_tokens["access_token"]

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
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.api
    @allure.step('Проверка адреса в сети ETH')
    def test_check_smoke_ether_ok(self, class_tokens):
        logger.info("Начинаю тест: проверка адреса в сети ETH")
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0xc8Bd2FBFe0437f38394C5d504221FC01CC8dF92a",
            "network": "ether"
        }

        access_token = class_tokens["access_token"]

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
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.api
    @allure.step('Проверка адреса в сети TRON')
    def test_check_smoke_tron_ok(self, class_tokens):
        logger.info("Начинаю тест: проверка адреса в сети TRON")

        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "TK9YEyYQS9H66S53eT78N2YnVpDmAy3qTV",
            "network": "tron"
        }

        access_token = class_tokens["access_token"]
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
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.api
    @allure.step('Негативная проверка неверного report_id')
    def test_smoke_negative_api_incorrect_report_id(self, class_tokens):

        logger.info("Начинаю негативный тест: проверка неверного report_id")
        access_token = class_tokens["access_token"]
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
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.api
    @allure.step('Негативная проверка протухшего токена авторизации')
    def test_smoke_negative_api_old_access_token(self, class_tokens):

        logger.info("Начинаю тест: протухшего access_token")
        access_token = class_tokens["access_token"]
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
        logger.info("Проверяю результат")

    # def test_check_120sec(self, tokens):
    #     url = f"{Constants.API_URL}/aml/check"
    #     payload = {
    #         "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
    #         "network": "btc"
    #     }
    #     headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    #
    #     requests.post(url, headers=headers, json=payload)
    #     response = requests.post(url, headers=headers, json=payload)
    #     data = response.json()
    #
    #     assert data["ok"] == 0


class TestCheckSmokeUI:
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.step('Позитивная проверка входа по email')
    def test_email_login_ui(self, login_page):
        logger.info("Начинаю тест: вход по email")
        login_page.open("https://check-dev.g5dl.com")

        login_page.enter_wallet_address("0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f")
        login_page.enter_email(Constants.EMAIL)
        code = get_verification_code()
        login_page.enter_code(code)

        login_page.check_final_result()
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.step('Негативная проверка что капча отрабатывает 120 сек паузы между отправкой кода')
    def test_incorrect_120sec_pause_ui(self, login_page):
        logger.info("Начинаю тест: пауза 120 сек")
        login_page.open("https://check-dev.g5dl.com")

        login_page.enter_wallet_address("0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f")
        login_page.enter_email(Constants.EMAIL)

        login_page.check_120sec_pause()
        logger.info("Проверяю результат")

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.step('Негативная проверка некорректного адреса (с замоканной авторизацией)')
    def test_incorrect_address_ui(self, login_page):
        login_page.open("https://check-dev.g5dl.com")
        login_page.enter_wallet_address("111111110x36b12020B741A111111111722Ca21a0ef2B9E8977f8715b4f")
        login_page.enter_incorrect_address()





    # @pytest.mark.smoke
    # @pytest.mark.ui
    # @allure.step('Негативная проверка некорректного адреса (с замоканной авторизацией)')
    # def test_incorrect_address_ui(self, login_page, mock_auth):
    #
    #     mock_auth(login_page.page)
    #     login_page.open("https://check-dev.g5dl.com")
    #
    #     login_page.enter_wallet_address("111111110x36b12020B741A111111111722Ca21a0ef2B9E8977f8715b4f")
    #     login_page.enter_email(Constants.MOCK_EMAIL)  # → мок /auth/login
    #     login_page.enter_code("000000")  # → мок /auth/verify-email
    #     login_page.click_check_for_free_button()
    #     login_page.wait_for_invalid_address_text()


        # @pytest.mark.smoke
        # @allure.step('Негативная проверка некорректного email')
        # def test_incorrect_email_ui(self, login_page):
        #     logger.info("Начинаю тест проверка некорректного email")
        #
        #     login_page.open("https://check-dev.g5dl.com")
        #
        #     login_page.enter_wallet_address("0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f")
        #     login_page.enter_invalid_email("oukb1147gmail.")
        #
        #     login_page.wait_for_invalid_email_text()
        #     logger.info("Проверяю результат")



