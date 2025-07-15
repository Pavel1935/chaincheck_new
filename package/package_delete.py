import requests
from Constants import Constants


class TestPackageDelete:
    def test_package_delete(self):

        url = Constants.API_URL + "/package"

        params = "19a4d297-d356-4fcc-ad57-057b74434f21"

        payload = {
        }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.delete(url, headers=headers, params=params, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
