
import requests
from Constants import Constants
from conftest import report_id
from conftest import class_tokens

RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
GREEN = "\033[32m"
BLUE = "\033[34m"
ORANGE = "\033[33m"
RED = "\033[31m"
YELLOW = "\033[93m"


class TestAmlCheckHistoryOne:
    def test_aml_check_history_one(self, class_tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
                "report_id": "ef0c5524-adc4-41f2-a857-00d7b95fd1cb"
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        risk_score = data["result"].get("risk_score")

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

    def test_aml_check_history_one_incorrect_report_id(self, class_tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
                "report_id": 123
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_history_one_without_report_id(self, class_tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        # payload = {
        #         "report_id": 123
        # }

        response = requests.post(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_history_one_invalid_access_token(self, class_tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyODI1OTQ2LCJuYmYiOjE3NTI3Mzk1NDYsImlhdCI6MTc1MjczOTU0NiwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.XFSxiHeRssn28oEY1VEBXi8IhmNF9apI23IXOZxLvF4"}

        payload = {
                "report_id": report_id
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"
