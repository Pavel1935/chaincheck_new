import requests
from Constants import Constants
from conftest import report_id
from conftest import tokens


class TestAmlCheckStatus:
    def test_aml_check_status(self, tokens, report_id):

        url = Constants.API_URL + "aml/check/status"
        access_token = tokens["access_token"]

        payload = {
          "report_id": report_id
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["status"]

    def test_aml_check_status_invalid_user_rights(self):

        url = Constants.API_URL + "aml/check/status"
        payload = {
          "report_id": "43ff6af3-d313-48df-aa79-e565823283e1"
        }

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5ODc5MDAtYmRlYS03YmVhLTlmMTktOGM4OTE4MDg4NDQ4IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NDc2MTA0LCJuYmYiOjE3NTQzODk3MDQsImlhdCI6MTc1NDM4OTcwNCwiZmluZ2VycHJpbnQiOiI4cUVYbEh6L01JOHI0bnZhL1JYcTVHd1Q5OGpGekNkbTVHTkVBaUxQS0drPSIsInVzZXJfcm9sZSI6MX0.dICvnss9m0EcshWDbaWDuy-4ywo3dCNvYkJY1lPH2q4"}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_USER_RIGHTS" or "REPORT_NOT_FOUND"

    def test_aml_check_status_invalid_access_token(self, report_id):

        url = Constants.API_URL + "aml/check/status"
        payload = {
          "report_id": report_id
        }

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyODI1OTQ2LCJuYmYiOjE3NTI3Mzk1NDYsImlhdCI6MTc1MjczOTU0NiwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.XFSxiHeRssn28oEY1VEBXi8IhmNF9apI23IXOZxLvF4"}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_aml_check_with_report_id(self, tokens):

        url = Constants.API_URL + "aml/check/status"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

