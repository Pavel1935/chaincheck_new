import requests
from Constants import Constants
from conftest import class_tokens


class TestAmlCheckHistoryLimit:
    def test_aml_check_history_limit(self, class_tokens):

        url = Constants.API_URL + "/aml/check/history"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}
        params = "limit=0"

        response = requests.get(url, headers=headers, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["result"]["items"]

    def test_aml_check_history_limit_empty_items(self):

        url = Constants.API_URL + "/aml/check/history"

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5ODc5MDAtYmRlYS03YmVhLTlmMTktOGM4OTE4MDg4NDQ4IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NDcwOTM2LCJuYmYiOjE3NTQzODQ1MzYsImlhdCI6MTc1NDM4NDUzNiwiZmluZ2VycHJpbnQiOiI4cUVYbEh6L01JOHI0bnZhL1JYcTVHd1Q5OGpGekNkbTVHTkVBaUxQS0drPSIsInVzZXJfcm9sZSI6MX0.bHCV-UB2ClOsoVeZxyAEt8FvlX4KOuXAgcazILS8weQ"}
        params = "limit=10"

        response = requests.get(url, headers=headers, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["result"] == {'items': []}

    def test_aml_check_history_invalid_limit(self, class_tokens):

        url = Constants.API_URL + "/aml/check/history"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}
        params = "limit=999999999999999999999999999999999999999999999999999999999999999999999999999999999999"

        response = requests.get(url, headers=headers, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_history_without_access_token(self, class_tokens):

        url = Constants.API_URL + "/aml/check/history"

        params = "limit=99"

        response = requests.get(url, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

