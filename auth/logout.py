import requests
from Constants import Constants


class TestLogout:

    def test_logout(self, access_token):
        endpoint = "/logout"
        url = Constants.API_URL + endpoint

        cookies = {
            "refresh_token": Constants.REFRESH_TOKEN
        }

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers, cookies=cookies, json={})
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1

