import requests
from Constants import Constants
from conftest import tokens


class TestPaymentCheck:
    def test_payment_check(self, tokens):
        external_payment_id = "8a383dc3-d43d-4f78-9bbf-3fa3c0e07270"

        url = f"{Constants.API_URL}/payment/check/{external_payment_id}"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.get(url, headers=headers)

        data = response.json()
        print("RESPONSE TEXT:", response.text)

        assert data["ok"] == 1
        assert data["status"] == "confirmed"

    def test_payment_check_without_external_payment_id(self, tokens):

        url = f"{Constants.API_URL}/payment/check/"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.get(url, headers=headers)

        data = response.json()
        print("RESPONSE TEXT:", response.text)

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_payment_check_invalid_external_payment_id(self, tokens):
        external_payment_id = "8a3831223dc3-d43d-4f78-9bbf-3fa3c0e07270"

        url = f"{Constants.API_URL}/payment/check/{external_payment_id}"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.get(url, headers=headers)

        data = response.json()
        print("RESPONSE TEXT:", response.text)

        assert data["ok"] == 0
        assert data["error"] == "ENTITY_NOT_FOUND"

    def test_payment_check_without_external_payment_id_data(self, tokens):
        external_payment_id = ""

        url = f"{Constants.API_URL}/payment/check/{external_payment_id}"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.get(url, headers=headers)

        data = response.json()
        print("RESPONSE TEXT:", response.text)

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_payment_check_old_access_token(self):
        external_payment_id = "8a383dc3-d43d-4f78-9bbf-3fa3c0e07270"
        url = f"{Constants.API_URL}/payment/check/{external_payment_id}"

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUxOTg5NTM4LCJuYmYiOjE3NTE5MDMxMzgsImlhdCI6MTc1MTkwMzEzOCwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.nMXEkTRqVial-Uz_2_OvrtVrHKrKxNLjgAqM128Oh4g"}

        response = requests.get(url, headers=headers)

        data = response.json()
        print("RESPONSE TEXT:", response.text)

        assert data["ok"] == 0
        assert data["status"] == "UNAUTHORIZED"

    def test_payment_check_invalid_access_token(self, tokens):
        external_payment_id = "8a383dc3-d43d-4f78-9bbf-3fa3c0e07270"

        url = f"{Constants.API_URL}/payment/check/{external_payment_id}"

        headers = {'Authorization': 'Bearer ' + "HiJohneyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NzI3Njk3LCJuYmYiOjE3NTQ2NDEyOTcsImlhdCI6MTc1NDY0MTI5NywiZmluZ2VycHJpbnQiOiJJTTA4Z1NyK3FhbnJDVkhMc2FnV1RBbnoxVlZ4NFVTVmxibDBnT2M2cldNPSIsInVzZXJfcm9sZSI6M30.YeOMYx4G-2A4Y_c5vnfLQpotk7lKCdjdwCvK2NmCCfA"}
        response = requests.get(url, headers=headers)

        data = response.json()
        print("RESPONSE TEXT:", response.text)

        assert data["ok"] == 0
        assert data["status"] == "BAD_REQUEST"

