import requests
from Constants import Constants



class TestLogin:
    def test_login(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "oukb1147@gmail.com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

