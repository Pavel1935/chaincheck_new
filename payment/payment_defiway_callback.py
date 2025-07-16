import requests
from Constants import Constants



class TestPaymentDefiwayCallback:
    def test_payment_defiway_callback(self):

        url = Constants.API_URL + "/payment/defiway/callback"

        payload = {
          "_id": "8a383dc3-d43d-4f78-9bbf-3fa3c0e07270"
        }

        # headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        response = requests.post(url, json=payload)

        assert response.status_code == 204
        assert response.text == ""
