import requests
from Constants import Constants
from conftest import get_access_token


class TestAmlCheck:
    def test_aml_check(self, get_access_token):

        url = Constants.API_URL + "aml/check"

        payload = {
              "wallet": "0x1234567890abcdef1234567890abcdef12345678",
              "network": "bsc"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_aml_check_organization(self, access_token):

        url = Constants.API_URL + "aml/check"

        payload = {
              "wallet": "0xE3e1147acD39687A25cA7716227c604500f5c31A",
              "network": "bsc"
            }
        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
