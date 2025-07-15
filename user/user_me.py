import requests
from Constants import Constants


class TestUserMe:

    def test_user_me(self):
        endpoint = "/user/me"
        url = Constants.API_URL + endpoint
        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["result"] == {
                "email": "oukb1147@gmail.com",
                "free_checks": 19,
                "id": "019010b4-a5fe-72f3-9eb5-3a8486b65865",
                "role": "admin",
                "username": ""
            }
        return response.cookies
