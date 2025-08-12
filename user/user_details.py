import requests
from Constants import Constants
from conftest import tokens


class TestDetails:

    def test_user_details(self, tokens):

        endpoint = "/user/detail"
        url = Constants.API_URL + endpoint
        access_token = tokens["access_token"]

        payload = {
            "email": Constants.EMAIL
        }

        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.post(url, json=payload, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["email"] == Constants.EMAIL

