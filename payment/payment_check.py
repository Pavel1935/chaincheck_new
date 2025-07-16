import requests
from Constants import Constants
from conftest import access_token



class TestPaymentCheck:
    def test_payment_check(self):

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        external_payment_id = "8a383dc3-d43d-4f78-9bbf-3fa3c0e07270"
        url = f"{Constants.API_URL}/payment/check/{external_payment_id}"

        response = requests.get(url, headers=headers)
        data = response.json()

        assert data.get("ok") == 1
        assert data.get("status") == "confirmed"
