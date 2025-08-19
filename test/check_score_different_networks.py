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
YELLOW = "\033[93m"


class TestCheckScore:
    report_id = None

    @pytest.mark.parametrize(
        "network,wallet",
        [
            ("btc", "bc1qffyax9rrxmqyq8xwjkzrrqwqjp3ppz5a4665f9"),  # 0-19
            ("btc", "bc1ph03gmlnmg4qmu4r5749qzw5aacye8tshyt85y5ckl5y2fztf5umspkswc9"),  # 20-39
            ("btc", "bc1qxlth5har0qasqvattsjvgp80st2x402u5shuud"),  # 40-59
            ("btc", "bc1ptf9aawj4gm6y0lu2vhmdvdp5428pck4q5zrrtf69vyl79ht3ufxqltjgp7"),  # 60-79
            ("btc", "bc1qy55d9w72vaj4apstgrtg866325pepsg8ck9t4m")  # 80-100
        ]
    )
    def test_risk_score_wallet_btc(self, network, wallet, tokens):
        access_token = tokens["access_token"]
        headers = {'Authorization': 'Bearer ' + access_token}

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

        if 0 <= risk_score < 20:
            print(f"{BOLD}{ITALIC}{GREEN}Низкий риск{RESET}")
        elif 20 <= risk_score < 40:
            print(f"{BOLD}{ITALIC}{BLUE}Умеренный риск{RESET}")
        elif 40 <= risk_score < 60:
            print(f"{BOLD}{ITALIC}{ORANGE}Средний риск{RESET}")
        elif 60 <= risk_score < 80:
            print(f"{BOLD}{ITALIC}{YELLOW}Высокий риск{RESET}")
        elif 80 <= risk_score <= 100:
            print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")

    @pytest.mark.parametrize(
        "network,wallet",
        [
            ("bsc", "0xB3764761E297D6f121e79C32A65829Cd1dDb4D32"),  # 0-19
            ("bsc", "0x34B35e19707d99283fc5003db8E30f2Fae833779"),  # 20-39
            ("bsc", "0xF90A6aFFC58416E5FD9670A6CdeBB79cA2A48E24"),  # 40-59
            ("bsc", "0x1663B74ABFB1768F4Be076C68aEdE84b1487CFE1"),  # 60-79
            ("bsc", "0x4562e14CBC31B73294dFE626ed22152964D96B9F")  # 80-100
        ]
    )
    def test_risk_score_wallet_bsc(self, network, wallet, tokens):

        access_token = tokens["access_token"]
        headers = {'Authorization': 'Bearer ' + access_token}

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
            print(f"{BOLD}{ITALIC}{YELLOW}Высокий риск{RESET}")
        elif 90 <= risk_score <= 100:
            print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")

    @pytest.mark.parametrize(
        "network,wallet",
        [
            ("ether", "0x617Ae9E20433e18f3f81FD62dd8667898542d1c5"),  # 0-19
            ("ether", "0xb0E62712d08d246C03EF19076dfbA56C355b4022"),  # 20-39
            ("ether", "0xc8Bd2FBFe0437f38394C5d504221FC01CC8dF92a"),  # 40-59
            ("ether", "0x1d39C2FDc5A939320109FFa48be2E356bcf253CF"),  # 60-79
            ("ether", "0xeD6e0A7e4Ac94D976eeBfB82ccf777A3c6baD921")  # 80-100
        ]
    )
    def test_risk_score_wallet_ether(self, network, wallet, tokens):
        access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer ' + access_token}

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
            print(f"{BOLD}{ITALIC}{YELLOW}Высокий риск{RESET}")
        elif 90 <= risk_score <= 100:
            print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")

    @pytest.mark.parametrize(
        "network,wallet",
        [
            ("tron", "TK4c76dEE6whmEw3yu57YmkMPGD8qacagX"),  # 0-19
            ("tron", "THfQd6TxV6s3cdw9sWa2aDvgSYkBio5aEf"),  # 20-39
            ("tron", "TXi4NvRDb2zTfTfbXgLFs1FsMSdgS8NoiQ"),  # 40-59
            ("tron", "TK9YEyYQS9H66S53eT78N2YnVpDmAy3qTV"),  # 60-79
            ("tron", "TEGDHgn5opDRvoSM5TcQ7vHcasknMDVEtY")  # 80-100
        ]
    )
    def test_risk_score_wallet_tron(self, network, wallet, tokens):
        access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer ' + access_token}

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
            print(f"{BOLD}{ITALIC}{YELLOW}Высокий риск{RESET}")
        elif 90 <= risk_score <= 100:
            print(f"{BOLD}{ITALIC}{RED}Критический риск{RESET}")

