import requests
from Constants import Constants


class TestPaymentDefiwayCallback:
    def test_payment_defiway_callback(self):

        url = Constants.API_URL + "/payment/defiway/callback"

        payload = {
          "_id": "e1943114-5b61-11f0-81fa-bae5a9a0c923"
        }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        assert response.status_code == 204

    def test_payment_defiway_callback_no_id(self):

        url = Constants.API_URL + "/payment/defiway/callback"

        response = requests.post(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_payment_defiway_callback_without_id(self):

        url = Constants.API_URL + "/payment/defiway/callback"

        payload = {
          "": "1943114-5b61-11f0-81fa-bae5a9a0c923"
        }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"
