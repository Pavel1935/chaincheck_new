import requests
from Constants import Constants



class TestPackagePut:
    def test_package_put(self):

        url = Constants.API_URL + "/package"

        payload = {
              "id": "19a4d297-d356-4fcc-ad57-057b74434f21",
              "title": "1",
              "price_usd": "11",
              "count_checks": 2,
              "ref_payout": "1",
              "status": 0
            }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
