import requests
from Constants import Constants
from conftest import tokens


class TestLogout:
    def test_logout(self, class_tokens):

        cookies = {
            "refresh_token": class_tokens["refresh_token"]
        }

        endpoint = "/logout"
        url = Constants.API_URL + endpoint

        headers = {
            "Authorization": f"Bearer {class_tokens['access_token']}"
        }

        response = requests.get(url, headers=headers, cookies=cookies, json={})
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_logout_without_refresh_token(self, class_tokens):

        # cookies = {
        #     "refresh_token": tokens["refresh_token"]
        # }

        endpoint = "/logout"
        url = Constants.API_URL + endpoint

        headers = {
            "Authorization": f"Bearer {class_tokens['access_token']}"
        }

        response = requests.get(url, headers=headers, json={})
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

