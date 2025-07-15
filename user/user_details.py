import requests
from Constants import Constants


class TestDetails:

    def test_user_details(self):
        endpoint = "/user/detail"
        url = Constants.API_URL + endpoint

        payload = {
            "email": Constants.EMAIL
        }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}
        response = requests.post(url, json=payload, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["email"] == "oukb1147@gmail.com"