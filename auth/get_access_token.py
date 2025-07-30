import requests
from Constants import Constants

class TestGetAccessToken:

    def test_get_access_token(self):

        url = "https://check-dev.g5dl.com/api/v1/auth/refresh-token"

        payload = ""
        headers = {
            'Cookie': 'refresh_token=01985bec-64b6-72ea-9c88-344a7ca3fcc2'
        }

        response = requests.post(url, headers=headers, data=payload)

        # response = requests.post(url)

        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1

