import time
import requests
from Constants import Constants
from conftest import tokens
from test.test_risk_score_1 import RESET

RESET="\033[0m"; BOLD="\033[1m"; ITALIC="\033[3m"
GREEN="\033[32m"; BLUE="\033[34m"; ORANGE="\033[33m"; RED="\033[31m";YELLOW = "\033[93m"


class TestCheckScore:
    report_id = None

    def test_aml_check(self, tokens):
        url = Constants.API_URL + "aml/check"
        payload = {
            "wallet": "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9",
            "network": "btc"
        }
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        time.sleep(1)

        TestCheckScore.report_id = data["result"]["report_id"]
        assert TestCheckScore.report_id

    def test_aml_check_history_one(self, tokens):
        assert TestCheckScore.report_id is not None, "report_id не установлен. test_aml_check должен запускаться первым."

        url = Constants.API_URL + "/aml/check/history/one"
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        payload = {"report_id": TestCheckScore.report_id}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

        risk_score = data["result"].get("risk_score")
        print("RISK SCORE:", risk_score)


        if risk_score <= 19:
            print(f"{BOLD}{ITALIC}{GREEN}Низкий риск{RESET}")
        elif risk_score <= 39:
            print(f"{BOLD}{ITALIC}{BLUE}Умеренный риск{RESET}")
        elif risk_score <= 59:
            print(f"{BOLD}{ITALIC}{ORANGE}Средний риск{RESET}")
        elif risk_score <= 79:
            print(f"{BOLD}{ITALIC}{YELLOW}Высокий риск{RESET}")
        else:
            print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")