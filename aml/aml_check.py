import requests
from Constants import Constants


class TestAmlCheck:
    def test_aml_check(self):

        url = Constants.API_URL + "aml/check"

        payload = {
              "wallet": "0x1234567890abcdef1234567890abcdef12345678",
              "network": "bsc"
            }
        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
