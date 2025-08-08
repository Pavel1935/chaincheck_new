import pytest
import requests
from Constants import Constants
from conftest import tokens



class TestPackagePut:
    def test_package_put(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "id": "72bf6f0f-7bb5-46bc-8e91-b7ff6e4bc663",
              "title": "1",
              "price_usd": "11",
              "count_checks": 2,
              "ref_payout": "1",
              "status": 0
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1

    @pytest.mark.parametrize(
        "data, value",
        [
            ("title", "в"),
            ("title", "привет"),
            ("title", "!:,.;/"),
            ("title", "123")
        ])
    def test_package_positive_title(self, tokens, data, value):
        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
            data: value,
            "count_checks": 100,
            "price_usd": "10",
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
