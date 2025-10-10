import pytest
import requests
from Constants import Constants
from conftest import verification_code_fixture

class TestVerifyEmail:
    def test_verify_email(self, verification_code_fixture):

        endpoint = "/auth/verify-email"
        url = Constants.API_URL + endpoint

        body = {
            "email": Constants.EMAIL,
            "code": "250516"
        }

        response = requests.post(url, json=body)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1

    def test_verify_email_without_code(self):

        endpoint = "/auth/verify-email"
        url = Constants.API_URL + endpoint

        body = {
            "email": Constants.EMAIL,
            "code": ""
        }

        response = requests.post(url, json=body)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_verify_email_incorrect_code(self):

        endpoint = "/auth/verify-email"
        url = Constants.API_URL + endpoint

        body = {
            "email": Constants.EMAIL,
            "code": "123456"
        }

        response = requests.post(url, json=body)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "ENTITY_NOT_FOUND"

    def test_verify_email_invalid_code(self):

        endpoint = "/auth/verify-email"
        url = Constants.API_URL + endpoint

        body = {
            "email": Constants.EMAIL,
            "code": "1234567890"
        }

        response = requests.post(url, json=body)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "ENTITY_NOT_FOUND"

