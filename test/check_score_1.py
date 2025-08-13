import pytest
import requests
import time
from Constants import Constants
from conftest import tokens

RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
GREEN = "\033[32m"
BLUE = "\033[34m"
ORANGE = "\033[33m"
RED = "\033[31m"

@pytest.mark.parametrize(
    "network,wallet",
    [
        ("btc", "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9"),  # 0-19
        ("btc", "bc1q9jr8hp4w9eze8l2a5yz6fwctmly2srwl48ymv3"),  # 20-39
        ("btc", "bc1qxlth5har0qasqvattsjvgp80st2x402u5shuud"),  # 40-59
        ("btc", "bc1qcvrsxq8entyeu7c4qkq2v904hc43cyg2x637jv"),  # 60-79
        ("btc", "bc1qw2kel623n947d0xagnaylswj20m2zgefdsxqm6")   # 80-100
    ]
)
def test_risk_score_wallet_btc(network, wallet, tokens):
    headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

    url_check = Constants.API_URL + "aml/check"
    payload = {"wallet": wallet, "network": network}
    response = requests.post(url_check, headers=headers, json=payload)
    data = response.json()
    assert data["ok"] == 1
    report_id = data["result"]["report_id"]

    time.sleep(1)

    url_history = Constants.API_URL + "/aml/check/history/one"
    response = requests.post(url_history, headers=headers, json={"report_id": report_id})
    data = response.json()
    assert data["ok"] == 1
    risk_score = data["result"].get("risk_score")

    print(f"\nАдрес: {wallet}")
    print(f"Оценка риска: {risk_score}")

    if risk_score <= 19:
        print(f"{BOLD}{ITALIC}{GREEN}Низкий риск{RESET}")
    elif 20 <= risk_score <= 39:
        print(f"{BOLD}{ITALIC}{BLUE}Умеренный риск{RESET}")
    elif 40 <= risk_score <= 59:
        print(f"{BOLD}{ITALIC}{ORANGE}Средний риск{RESET}")
    elif 60 <= risk_score <= 79:
        print(f"{BOLD}{ITALIC}{RED}Высокий риск{RESET}")
    elif 90 <= risk_score <= 100:
        print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")

    @pytest.mark.parametrize(
        "network,wallet",
        [
            ("evm", ""),  # 0-19
            ("evm", ""),  # 20-39
            ("evm", ""),  # 40-59
            ("evm", ""),  # 60-79
            ("evm", "")  # 80-100
        ]
    )
    def test_risk_score_wallet_evm(network, wallet, tokens):
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

        url_check = Constants.API_URL + "aml/check"
        payload = {"wallet": wallet,
                   "network": network
                   }

        response = requests.post(url_check, headers=headers, json=payload)

        data = response.json()
        assert data["ok"] == 1
        report_id = data["result"]["report_id"]

        time.sleep(1)

        url_history = Constants.API_URL + "/aml/check/history/one"
        response = requests.post(url_history, headers=headers, json={"report_id": report_id})
        data = response.json()
        assert data["ok"] == 1
        risk_score = data["result"].get("risk_score")

        print(f"\nАдрес: {wallet}")
        print(f"Оценка риска: {risk_score}")

        if risk_score <= 19:
            print(f"{BOLD}{ITALIC}{GREEN}Низкий риск{RESET}")
        elif 20 <= risk_score <= 39:
            print(f"{BOLD}{ITALIC}{BLUE}Умеренный риск{RESET}")
        elif 40 <= risk_score <= 59:
            print(f"{BOLD}{ITALIC}{ORANGE}Средний риск{RESET}")
        elif 60 <= risk_score <= 79:
            print(f"{BOLD}{ITALIC}{RED}Высокий риск{RESET}")
        elif 90 <= risk_score <= 100:
            print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")


