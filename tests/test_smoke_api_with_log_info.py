import time
import requests
import logging
import pytest
from Constants import Constants

log = logging.getLogger(__name__)
BASE = Constants.API_URL


class TestAMLCheckSmoke:
    @pytest.mark.smoke
    def test_aml_check_smoke_btc_ok(self, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url = f"{BASE}/aml/check"

        payload = {
            "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
            "network": "btc"
        }

        # --- шаг 1: запуск AML-проверки ---
        log.info("POST %s — запуск AML-проверки (BTC)", url)
        log.debug("Payload: %s", payload)

        t0 = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        dt = (time.time() - t0) * 1000
        log.info("Response %s %s, %.0f ms", url, response.status_code, dt)

        try:
            data = response.json()
        except Exception:
            log.error("Non-JSON response: %s", response.text[:500])
            raise

        assert data.get("ok") == 1, f"/aml/check failed: {data}"
        report_id = data["result"]["report_id"]
        log.info("Получен report_id=%s", report_id)

        # --- шаг 2: проверка истории ---
        time.sleep(1)
        url_history = f"{BASE}/aml/check/history/one"
        log.info("POST %s — получение результата по report_id=%s", url_history, report_id)

        t1 = time.time()
        response2 = requests.post(url_history, headers=headers, json={"report_id": report_id}, timeout=10)
        dt2 = (time.time() - t1) * 1000
        log.info("Response %s %s, %.0f ms", url_history, response2.status_code, dt2)

        data2 = response2.json()
        assert data2.get("ok") == 1, f"/aml/check/history/one failed: {data2}"


    @pytest.mark.smoke
    def test_aml_check_smoke_bsc_ok(self, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url = f"{BASE}/aml/check"

        payload = {
            "wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b",
            "network": "bsc"
        }

        log.info("POST %s — запуск AML-проверки (BSC)", url)
        log.debug("Payload: %s", payload)

        t0 = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        dt = (time.time() - t0) * 1000
        log.info("Response %s %s, %.0f ms", url, response.status_code, dt)

        data = response.json()
        assert data.get("ok") == 1, f"/aml/check failed: {data}"
        report_id = data["result"]["report_id"]
        log.info("Получен report_id=%s", report_id)

        time.sleep(1)
        url_history = f"{BASE}/aml/check/history/one"
        log.info("POST %s — получение результата по report_id=%s", url_history, report_id)

        response2 = requests.post(url_history, headers=headers, json={"report_id": report_id}, timeout=10)
        log.info("Response %s %s", url_history, response2.status_code)

        data2 = response2.json()
        assert data2.get("ok") == 1, f"/aml/check/history/one failed: {data2}"


    @pytest.mark.smoke
    def test_aml_check_smoke_ether_ok(self, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url = f"{BASE}/aml/check"

        payload = {
            "wallet": "0xc8Bd2FBFe0437f38394C5d504221FC01CC8dF92a",
            "network": "ether"
        }

        log.info("POST %s — запуск AML-проверки (Ether)", url)
        log.debug("Payload: %s", payload)

        t0 = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        dt = (time.time() - t0) * 1000
        log.info("Response %s %s, %.0f ms", url, response.status_code, dt)

        data = response.json()
        assert data.get("ok") == 1, f"/aml/check failed: {data}"
        report_id = data["result"]["report_id"]
        log.info("Получен report_id=%s", report_id)

        time.sleep(1)
        url_history = f"{BASE}/aml/check/history/one"
        log.info("POST %s — получение результата по report_id=%s", url_history, report_id)

        response2 = requests.post(url_history, headers=headers, json={"report_id": report_id}, timeout=10)
        log.info("Response %s %s", url_history, response2.status_code)

        data2 = response2.json()
        assert data2.get("ok") == 1, f"/aml/check/history/one failed: {data2}"


    @pytest.mark.smoke
    def test_aml_check_smoke_tron_ok(self, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url = f"{BASE}/aml/check"

        payload = {
            "wallet": "TK9YEyYQS9H66S53eT78N2YnVpDmAy3qTV",
            "network": "tron"
        }

        log.info("POST %s — запуск AML-проверки (TRON)", url)
        log.debug("Payload: %s", payload)

        t0 = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        dt = (time.time() - t0) * 1000
        log.info("Response %s %s, %.0f ms", url, response.status_code, dt)

        data = response.json()
        assert data.get("ok") == 1, f"/aml/check failed: {data}"
        report_id = data["result"]["report_id"]
        log.info("Получен report_id=%s", report_id)

        time.sleep(1)
        url_history = f"{BASE}/aml/check/history/one"
        log.info("POST %s — получение результата по report_id=%s", url_history, report_id)

        response2 = requests.post(url_history, headers=headers, json={"report_id": report_id}, timeout=10)
        log.info("Response %s %s", url_history, response2.status_code)

        data2 = response2.json()
        assert data2.get("ok") == 1, f"/aml/check/history/one failed: {data2}"


    @pytest.mark.smoke
    def test_smoke_negative_api_incorrect_report_id(self, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url = f"{BASE}/aml/check"

        payload = {"wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9", "network": "btc"}

        log.info("POST %s — запуск AML-проверки (negative, bad report_id)", url)
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        assert data["ok"] == 1
        report_id = 123  # заведомо неверный
        log.info("Задаём некорректный report_id=%s", report_id)

        time.sleep(1)
        url_history = f"{BASE}/aml/check/history/one"
        response2 = requests.post(url_history, headers=headers, json={"report_id": report_id}, timeout=10)
        log.info("Response %s %s", url_history, response2.status_code)

        data2 = response2.json()
        assert data2["ok"] == 0
        assert data2["error"] == "BAD_REQUEST"


    @pytest.mark.smoke
    def test_smoke_negative_api_old_access_token(self, tokens):
        valid_headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        url = f"{BASE}/aml/check"

        payload = {"wallet": "0x1EDbA89FF829c4DF84b15F1D9Dd75DC9a5582F2b", "network": "bsc"}

        log.info("POST %s — запуск AML-проверки (negative, old token)", url)
        response = requests.post(url, headers=valid_headers, json=payload, timeout=10)
        data = response.json()
        assert data["ok"] == 1
        report_id = data["result"]["report_id"]
        log.info("Получен report_id=%s", report_id)

        time.sleep(1)
        url_history = f"{BASE}/aml/check/history/one"

        old_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # твой протухший токен
        headers_old = {'Authorization': f'Bearer {old_token}'}

        log.info("POST %s — проверка истории с просроченным токеном", url_history)
        response2 = requests.post(url_history, headers=headers_old, json={"report_id": report_id}, timeout=10)
        log.info("Response %s %s", url_history, response2.status_code)

        data2 = response2.json()
        assert data2["ok"] == 0
        assert data2["error"] == "UNAUTHORIZED"