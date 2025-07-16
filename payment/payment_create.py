import requests
from Constants import Constants



class TestPaymentCreate:
    def test_payment_create(self):

        url = Constants.API_URL + "/payment/create"

        payload = {
          "package_id": "095a5476-2e17-4677-a91b-06be1e336949",
          "promo_code": "oioioi",
          "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}
        # headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["url"].startswith("https")
