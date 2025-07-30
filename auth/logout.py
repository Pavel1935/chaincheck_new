import requests
from Constants import Constants
# from conftest import tokens


class TestLogout:

    def test_logout(self, tokens):

        cookies = {
            "refresh_token": tokens["refresh_token"]
        }

        endpoint = "/logout"
        url = Constants.API_URL + endpoint

        headers = {
            "Authorization": f"Bearer {tokens['access_token']}"
        }

        response = requests.get(url, headers=headers, cookies=cookies, json={})
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1

