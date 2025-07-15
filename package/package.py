import requests
from Constants import Constants
from conftest import report_id


class TestPackage:
    def test_package(self):

        url = Constants.API_URL + "/package"

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
