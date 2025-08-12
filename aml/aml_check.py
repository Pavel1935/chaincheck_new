import pytest
import requests
from Constants import Constants
from conftest import tokens
from conftest import get_access_token


class TestAmlCheck:
    @pytest.mark.parametrize(
        "network,wallet",
        [
            ("btc", "bc1q29k0jkvpekcuv6dwchjww8pev92gsxe9uw24wz"),
            ("bsc", "0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f"),
            ("ether", "0xDC60CF09199b3ccdbD9d9f6920829d5496FC3d04"),
            ("tron", "TFazJsQKQd8J1ryoogBnH6kkwm951rscHa"),
        ]
    )
    def test_aml_check(self, tokens, network, wallet):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": wallet,
            "network": network
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["report_id"]

    def test_aml_check_blacklist_risk(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x489A8756C18C0b8B24EC2a2b9FF3D4d447F79BEc",
            "network": "ether"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["report_id"]

    def test_aml_check_tron(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "TFazJsQKQd8J1ryoogBnH6kkwm951rscHa",
            "network": "tron"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["report_id"]

    def test_aml_check_btc(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "bc1q29k0jkvpekcuv6dwchjww8pev92gsxe9uw24wz",
            "network": "btc"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["report_id"]

    def test_aml_check_incorrect_network(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "bc1q29k0jkvpekcuv6dwchjww8pev92gsxe9uw24wz",
            "network": "tron"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_ADDRESS"

    def test_aml_check_organization(self, tokens):

        url = Constants.API_URL + "aml/check"

        payload = {
              "wallet": "0xE3e1147acD39687A25cA7716227c604500f5c31A",
              "network": "bsc"
            }
        access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["report_id"]

    def test_aml_check_invalid__data_wallet(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0xE3e1147acD39687A25cA7716227c604500f5c31Akjg;jr",
            "network": "bsc"
        }
        access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_ADDRESS"

    def test_aml_check_invalid_data_network(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1234567890gwrgwrtabcdef1234567890abcdef12345678",
            "network": "123"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_NETWORK"


    def test_aml_check_invalid_network_and_wallet(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1234ergege567890gwrgwrtabcdef1234567890abcdef12345678",
            "network": "123"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_NETWORK"

    def test_aml_check_invalid_access_token(self):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1234567890abcdef1234567890abcdef12345678",
            "network": "bsc"
        }
        # access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NDY3MDU2LCJuYmYiOjE3NTQzODA2NTYsImlhdCI6MTc1NDM4MDY1NiwiZmluZ2VycHJpbnQiOiJJTTA4Z1NyK3FhbnJDVkhMc2FnV1RBbnoxVlZ4NFVTVmxibDBnT2M2cldNPSIsInVzZXJfcm9sZSI6M30.2K58QMW5j7mYCG2l7EwJn-hiG-2twPUck7RNMo5YGzk'}
        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_aml_check_without_access_token(self):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1234567890abcdef1234567890abcdef12345678",
            "network": "bsc"
        }
        # access_token = tokens["access_token"]
        headers = {'Authorization': f'Bearer ""'}
        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_aml_check_without_wallet(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            # "wallet": "0x1234567890abcdef1234567890abcdef12345678",
            "network": "bsc"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_invalid_network(self, tokens):
        url = Constants.API_URL + "aml/check"

        payload = {
            "wallet": "0x1234567890abcdef1234567890abcdef12345678",
            "netqwork": "bsc"
        }

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_without_payload(self, tokens):
        url = Constants.API_URL + "aml/check"

        access_token = tokens["access_token"]

        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

