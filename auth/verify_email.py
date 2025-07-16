import pytest
import requests
from Constants import Constants
from conftest import generate_email, verification_code

class TestVerifyEmail:
    def test_verify_email(self):

        endpoint = "/Auth/verify-email"
        url = Constants.API_URL + endpoint

        body = {
            "email": Constants.EMAIL,
            "code": "445461"
        }

        response = requests.post(url, json=body)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
