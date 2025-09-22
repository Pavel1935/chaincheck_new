import requests
from conftest import tokens

class TestGetAccessToken:

    def test_get_access_token(self, tokens):

        url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"
        refresh_token = tokens["refresh_token"]

        payload = ""
        headers = {
            'Cookie': f'refresh_token={refresh_token}'
        }

        response = requests.post(url, headers=headers, data=payload)

        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_get_access_token_invalid_refresh(self):

        url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"

        payload = ""
        headers = {
            'Cookie': 'refresh_token=0197c5ba-301b-7d17-a197-e71f67dbce5c'
        }

        response = requests.post(url, headers=headers, data=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "ENTITY_NOT_FOUND"


    def test_get_access_token_without_refresh(self):

        url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"

        payload = ""
        headers = {
            'Cookie': ''
        }

        response = requests.post(url, headers=headers, data=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"
