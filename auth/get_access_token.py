import requests
from Constants import Constants

class TestGetAccessToken:

    def test_get_access_token(self):

        url = Constants.API_URL + "/auth/refresh-token"

        cookies = {
            "refresh_token": Constants.REFRESH_TOKEN
        }

        response = requests.post(url, cookies=cookies)

        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1

