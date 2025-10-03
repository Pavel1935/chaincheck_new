import requests
from Constants import Constants
from conftest import class_tokens


class TestUserMe:

    def test_user_me(self, class_tokens):

        endpoint = "/user/me"
        url = Constants.API_URL + endpoint
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["result"]["email"] == Constants.EMAIL

    def test_user_me_without_token(self, class_tokens):

        endpoint = "/user/me"
        url = Constants.API_URL + endpoint

        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_user_me_incorrect_token(self, class_tokens):

        endpoint = "/user/me"
        url = Constants.API_URL + endpoint

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUxOTg5NTM4LCJuYmYiOjE3NTE5MDMxMzgsImlhdCI6MTc1MTkwMzEzOCwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.nMXEkTRqVial-Uz_2_OvrtVrHKrKxNLjgAqM128Oh4g"}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_user_me_invalid_token(self, class_tokens):

        endpoint = "/user/me"
        url = Constants.API_URL + endpoint

        headers = {'Authorization': 'Bearer ' + "HiJohneyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUxOTg5NTM4LCJuYmYiOjE3NTE5MDMxMzgsImlhdCI6MTc1MTkwMzEzOCwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.nMXEkTRqVial-Uz_2_OvrtVrHKrKxNLjgAqM128Oh4g"}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_user_me_without_data_token(self, class_tokens):

        endpoint = "/user/me"
        url = Constants.API_URL + endpoint

        headers = {'Authorization': 'Bearer ' + ""}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

