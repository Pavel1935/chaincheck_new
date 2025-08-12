import time
from numbers import Real
from tkinter.font import BOLD, ITALIC
from conftest import tokens
import pytest
import requests
from math import isfinite

from Constants import Constants
# если хочешь цвета ANSI, раскомментируй:
RESET="\033[0m"; BOLD="\033[1m"; ITALIC="\033[3m"
GREEN="\033[32m"; BLUE="\033[34m"; ORANGE="\033[33m"; RED="\033[31m"


class TestCheckScore:
    # @pytest.mark.parametrize(
    #     "network,wallet",
    #     [
    #         # 0 - 19
    #         ("btc", "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9"),
    #         # 20 - 39
    #         ("btc", "bc1q9jr8hp4w9eze8l2a5yz6fwctmly2srwl48ymv3"),
    #         # 40 - 59
    #         ("btc", "bc1qxlth5har0qasqvattsjvgp80st2x402u5shuud"),
    #         # 60 - 79
    #         ("btc", "bc1qcvrsxq8entyeu7c4qkq2v904hc43cyg2x637jv"),
    #         # 79 - 100
    #         ("btc", "bc1qw2kel623n947d0xagnaylswj20m2zgefdsxqm6")
    #     ]
    # )
    #
    # def test_check_score(self, tokens, network, wallet):
    #     url = Constants.API_URL + "aml/check"
    #     url = Constants.API_URL + "/aml/check/history/one"
    #
    #     payload = {
    #         "wallet": wallet,
    #         "network": network
    #     }
    #
    #     access_token = tokens["access_token"]
    #
    #     headers = {'Authorization': 'Bearer ' + access_token}
    #     response = requests.post(url, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #
    #     data = response.json()
    #     time.sleep(1)
    #
    #     return data["result"]["report_id"]
    #
    #     payload = {
    #         "report_id": "report_id"
    #     }
    #
    #     response = requests.post(url, headers=headers, json=payload)
    #     print("RESPONSE TEXT:", response.text)
    #
    #     data = response.json()
    #     score = data["result"]["risk_score"]
    #
    #     if score <= 39:
    #         print(f"{BOLD}{ITALIC}{GREEN}Низкий риск{RESET}")
    #     elif 40 <= score <= 59:
    #         print(f"{BOLD}{ITALIC}{BLUE}Умеренный риск{RESET}")
    #     elif 60 <= score <= 79:
    #         print(f"{BOLD}{ITALIC}{ORANGE}Высокий риск{RESET}")
    #     elif score >= 80:
    #         print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")
    #
    #     assert data["ok"] == 1

    import pytest
    import requests
    import time

    class TestCheckScore:
        @pytest.mark.parametrize(
            "network,wallet",
            [
                ("btc", "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9"),
                ("btc", "bc1q9jr8hp4w9eze8l2a5yz6fwctmly2srwl48ymv3"),
                ("btc", "bc1qxlth5har0qasqvattsjvgp80st2x402u5shuud"),
                ("btc", "bc1qcvrsxq8entyeu7c4qkq2v904hc43cyg2x637jv"),
                ("btc", "bc1qw2kel623n947d0xagnaylswj20m2zgefdsxqm6"),
            ]
        )
        def test_check_score(self, tokens, network, wallet):
            url_check = Constants.API_URL + "aml/check"
            url_result = Constants.API_URL + "aml/check/history/one"  # <- проверь в доках!
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}

            # 1) Стартуем проверку
            resp = requests.post(url_check, headers=headers, json={"wallet": wallet, "network": network})
            assert resp.ok, f"check failed: {resp.status_code} {resp.text}"
            data = resp.json()
            assert data.get("ok") == 1, f"check not ok: {data}"
            report_id = data["result"]["report_id"]

            # 2) Ждём готовности и получаем результат
            last = None
            for _ in range(10):  # до 10 попыток
                time.sleep(1)
                resp2 = requests.post(url_result, headers=headers, json={"report_id": report_id})
                assert resp2.ok, f"result failed: {resp2.status_code} {resp2.text}"
                last = resp2.json()
                if last.get("ok") == 1 and "risk_score" in last.get("result", {}):
                    break
            else:
                pytest.fail(f"report not ready: {last}")

            score = last["result"]["risk_score"]
            assert isinstance(score, Real), f"unexpected score type: {type(score)}"

            if score <= 39:
                print(f"{BOLD}{ITALIC}{GREEN}Низкий риск{RESET}")
            elif 40 <= score <= 59:
                print(f"{BOLD}{ITALIC}{BLUE}Умеренный риск{RESET}")
            elif 60 <= score <= 79:
                print(f"{BOLD}{ITALIC}{ORANGE}Высокий риск{RESET}")
            elif score >= 80:
                print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")

            assert data["ok"] == 1
            # твоя логика интерпретации риска — ок, по желанию



