import requests
from Constants import Constants
from conftest import report_id
from conftest import tokens


class TestAmlCheckHistoryOne:
    def test_aml_check_history_one(self, tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
                "report_id": report_id
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["id"]

    def test_aml_check_history_one_incorrect_report_id(self, tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
                "report_id": 123
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_history_one_without_report_id(self, tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        # payload = {
        #         "report_id": 123
        # }

        response = requests.post(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_history_one_invalid_access_token(self, tokens, report_id):

        url = Constants.API_URL + "/aml/check/history/one"

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyODI1OTQ2LCJuYmYiOjE3NTI3Mzk1NDYsImlhdCI6MTc1MjczOTU0NiwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.XFSxiHeRssn28oEY1VEBXi8IhmNF9apI23IXOZxLvF4"}

        payload = {
                "report_id": 123
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"
