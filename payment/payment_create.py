import pytest
import requests
from Constants import Constants
from conftest import tokens


class TestPaymentCreate:
    def test_payment_create(self, tokens):

        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
          "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
          "promo_code": "oioioi",
          "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["url"].startswith("https")

    @pytest.mark.parametrize(
        "data, value",
        [
            ("promo_code", "123"),
            ("promo_code", "ф"),
            ("promo_code", "Спартак"),
            ("promo_code", "")
        ])

    def test_payment_create_positive_promo_code(self, tokens, data, value):

        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
            "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
            data: value,
            "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["url"].startswith("https")

    @pytest.mark.parametrize(
        "data_3, value_3",
        [
            ("package_id", "helloworldcb93f53f-7b22-4a7c-bc43-6552db486cc6"),
            ("package_id", 123),
            ("package_id", "123"),
            ("package_id", "приветмир"),
            ("package_id", ""),
            ("package_id", "%:,."),
            ("package_id", "d"),
            ("package_id", "  ")
        ])
    def test_payment_create_negative_package_id(self, tokens, data_3, value_3):
        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
            data_3: value_3,
            "promo_code": "oioioi",
            "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "VALIDATION_PAYMENT_SERVICE" or "BAD_REQUEST"

    @pytest.mark.parametrize(
        "data_1, value_1",
        [
            ("payment_service", "DEFIWAY"),
            ("payment_service", "123"),
            ("payment_service", "дефивей"),
            ("payment_service", ""),
            ("payment_service", "%:,."),
            ("payment_service", "d"),
            ("payment_service", "  ")
        ])
    def test_payment_create_negative_payment_service(self, tokens, data_1, value_1):
        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
            "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
            "promo_code": "oioioi",
            data_1: value_1
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "VALIDATION_PAYMENT_SERVICE" or "BAD_REQUEST"

    @pytest.mark.parametrize(
        "data_4, value_4",
        [
            ("promo_code", 123)
        ])

    def test_payment_create_negative_promo_code(self, tokens, data_4, value_4):

        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
            "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
            data_4: value_4,
            "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "VALIDATION_PAYMENT_SERVICE" or "BAD_REQUEST"

    def test_payment_create_without_promo_code(self, tokens):

        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
          "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
          "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["url"].startswith("https")

    def test_payment_create_without_package_id(self, tokens):

        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
          "promo_code": "oioioi",
          "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_payment_create_without_payment_service(self, tokens):

        url = Constants.API_URL + "/payment/create"
        access_token = tokens["access_token"]

        payload = {
          "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
          "promo_code": "oioioi",
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_payment_create_without_access_token(self):

        url = Constants.API_URL + "/payment/create"

        payload = {
          "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
          "promo_code": "oioioi",
          "payment_service": "defiway"
        }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_payment_create_old_access_token(self, tokens):

        url = Constants.API_URL + "/payment/create"

        payload = {
          "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
          "promo_code": "oioioi",
          "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUxOTg5NTM4LCJuYmYiOjE3NTE5MDMxMzgsImlhdCI6MTc1MTkwMzEzOCwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.nMXEkTRqVial-Uz_2_OvrtVrHKrKxNLjgAqM128Oh4g"}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_payment_create_old_access_token(self, tokens):

        url = Constants.API_URL + "/payment/create"

        payload = {
          "package_id": "cb93f53f-7b22-4a7c-bc43-6552db486cc6",
          "promo_code": "oioioi",
          "payment_service": "defiway"
        }

        headers = {'Authorization': 'Bearer ' + "helloworldeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NzQ4MjMxLCJuYmYiOjE3NTQ2NjE4MzEsImlhdCI6MTc1NDY2MTgzMSwiZmluZ2VycHJpbnQiOiJJTTA4Z1NyK3FhbnJDVkhMc2FnV1RBbnoxVlZ4NFVTVmxibDBnT2M2cldNPSIsInVzZXJfcm9sZSI6M30.GZEz5ASNNPr6a6hEW142fXLPNvBYwjeqEAS-cKFR0nc"}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

