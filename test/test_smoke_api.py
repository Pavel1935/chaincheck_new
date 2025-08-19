import pytest
import requests
import time
from Constants import Constants
from conftest import tokens
import logging

log = logging.getLogger(__name__)
BASE = Constants.API_URL.rstrip("/")


class TestSmokeApi:

    @pytest.mark.smoke
    def test_aml_check_smoke_btc_ok(self, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url_check = f"{BASE}/aml/check"

        payload = {
            "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
            "network": "btc"
        }

        # ③ до запроса: фиксируем намерение + ключевые входные данные
        #    (это помогает понять «что именно тест пытался сделать»)
        log.info("POST %s — запуск AML-проверки (BTC)", url_check)
        log.debug("Payload: %s", payload)  # в DEBUG можно логировать подробности

        t0 = time.time()
        response = requests.post(url_check, headers=headers, json=payload, timeout=10)
        dt = (time.time() - t0) * 1000

        # ④ сразу после ответа: статус, длительность, краткий фрагмент ответа
        #    (три вещи, которые нужны при любой диагностике)
        log.info("Response %s %s, %.0f ms", url_check, response.status_code, dt)
        try:
            data = response.json()
        except Exception:
            # ⑤ на случай неожиданного формата ответа — понятно, что вернул сервер
            log.error("Non-JSON response: %s", response.text[:500])
            raise

        # ⑥ проверяем контракт и даём содержательное сообщение, если упало
        assert data.get("ok") == 1, f"/aml/check failed: {data}"
        report_id = data["result"]["report_id"]

        # ⑦ логируем ключевой ID — это главный «трейс»,
        #    по которому можно пойти в бэковые логи/мониторинг
        log.info("Получен report_id=%s", report_id)

        # --- временное ожидание (ты позже заменишь на polling) ---
        time.sleep(1)

        url_history = f"{BASE}/aml/check/history/one"

        # ⑧ отдельный лог перед вторым шагом — чтобы в логах
        #    было видно, на каком именно шаге произошла ошибка
        log.info("POST %s — получение результата по report_id=%s", url_history, report_id)

        t1 = time.time()
        response2 = requests.post(url_history, headers=headers, json={"report_id": report_id}, timeout=10)
        dt2 = (time.time() - t1) * 1000

        log.info("Response %s %s, %.0f ms", url_history, response2.status_code, dt2)
        data2 = response2.json()

        # ⑨ финальная проверка + лог на случай падения
        assert data2.get("ok") == 1, f"/aml/check/history/one failed: {data2}"

    # @pytest.mark.smoke
    # def test_aml_check_smoke_btc_ok(self, tokens):
    #     log.info("Отправляю /aml/check для BTC")
    #     url = Constants.API_URL + "aml/check"
    #
    #     payload = {
    #         "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
    #         "network": "btc"
    #     }
    #
    #     access_token = tokens["access_token"]
    #
    #     headers = {'Authorization': f'Bearer {access_token}'}
    #
    #     response = requests.post(url, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #     data = response.json()
    #     assert data["ok"] == 1
    #     report_id = data["result"]["report_id"]
    #
    #     time.sleep(1)
    #
    #     url_check = Constants.API_URL + "/aml/check/history/one"
    #     response = requests.post(url_check, headers=headers, json={"report_id": report_id})
    #     data = response.json()
    #     assert data["ok"] == 1
    #
    # @pytest.mark.smoke
    # def test_aml_check_smoke_bsc_ok(self, tokens):
    #     url = Constants.API_URL + "aml/check"
    #
    #     payload = {
    #         "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
    #         "network": "bsc"
    #     }
    #
    #     access_token = tokens["access_token"]
    #
    #     headers = {'Authorization': f'Bearer {access_token}'}
    #
    #     response = requests.post(url, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #     data = response.json()
    #     assert data["ok"] == 1
    #     report_id = data["result"]["report_id"]
    #
    #     time.sleep(1)
    #
    #     url_check = Constants.API_URL + "/aml/check/history/one"
    #     response = requests.post(url_check, headers=headers, json={"report_id": report_id})
    #     data = response.json()
    #     assert data["ok"] == 1
    #
    # @pytest.mark.smoke
    # def test_aml_check_smoke_ether_ok(self, tokens):
    #     url = Constants.API_URL + "aml/check"
    #
    #     payload = {
    #         "wallet": "0xc8Bd2FBFe0437f38394C5d504221FC01CC8dF92a",
    #         "network": "ether"
    #     }
    #
    #     access_token = tokens["access_token"]
    #
    #     headers = {'Authorization': f'Bearer {access_token}'}
    #
    #     response = requests.post(url, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #     data = response.json()
    #     assert data["ok"] == 1
    #     report_id = data["result"]["report_id"]
    #
    #     time.sleep(1)
    #
    #     url_check = Constants.API_URL + "/aml/check/history/one"
    #     response = requests.post(url_check, headers=headers, json={"report_id": report_id})
    #     data = response.json()
    #     assert data["ok"] == 1
    #
    # @pytest.mark.smoke
    # def test_aml_check_smoke_tron_ok(self, tokens):
    #     url = Constants.API_URL + "aml/check"
    #
    #     payload = {
    #         "wallet": "TK9YEyYQS9H66S53eT78N2YnVpDmAy3qTV",
    #         "network": "tron"
    #     }
    #
    #     access_token = tokens["access_token"]
    #
    #     headers = {'Authorization': f'Bearer {access_token}'}
    #
    #     response = requests.post(url, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #     data = response.json()
    #     assert data["ok"] == 1
    #     report_id = data["result"]["report_id"]
    #
    #     time.sleep(1)
    #
    #     url_check = Constants.API_URL + "/aml/check/history/one"
    #     response = requests.post(url_check, headers=headers, json={"report_id": report_id})
    #     data = response.json()
    #     assert data["ok"] == 1
    #
    # @pytest.mark.smoke
    # def test_smoke_negative_api_incorrect_report_id(self, tokens):
    #     access_token = tokens["access_token"]
    #     headers = {'Authorization': 'Bearer ' + access_token}
    #
    #     url_check = Constants.API_URL + "aml/check"
    #     payload = {
    #         "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
    #         "network": "btc"
    #     }
    #
    #     response = requests.post(url_check, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #     data = response.json()
    #     assert data["ok"] == 1
    #     report_id = 123
    #
    #     time.sleep(1)
    #
    #     url_history = Constants.API_URL + "/aml/check/history/one"
    #     response = requests.post(url_history, headers=headers, json={"report_id": report_id})
    #     print("RESPONSE TEXT:", response.text)
    #
    #     data = response.json()
    #     assert data["ok"] == 0
    #     assert data["error"] == "BAD_REQUEST"
    #
    # @pytest.mark.smoke
    # def test_smoke_negative_api_old_access_token(self, tokens):
    #     access_token = tokens["access_token"]
    #     headers_1 = {'Authorization': 'Bearer ' + access_token}
    #
    #     url_check = Constants.API_URL + "aml/check"
    #     payload = {
    #         "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
    #         "network": "bsc"
    #     }
    #
    #     response = requests.post(url_check, headers=headers_1, json=payload)
    #     data = response.json()
    #     assert data["ok"] == 1
    #     report_id = data["result"]["report_id"]
    #
    #     time.sleep(1)
    #
    #     url_history = Constants.API_URL + "/aml/check/history/one"
    #     headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyMjE3NzUyLCJuYmYiOjE3NTIxMzEzNTIsImlhdCI6MTc1MjEzMTM1MiwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.T6qR_3EkMX4_1uBDdV8vM7GXqfbZzcaakDRuxxkgiAU"}
    #     response = requests.post(url_history, headers=headers,
    #                              json={"report_id": report_id})
    #     print("RESPONSE TEXT:", response.text)
    #
    #     data = response.json()
    #     assert data["ok"] == 0
    #     assert data["error"] == "UNAUTHORIZED"
    #
