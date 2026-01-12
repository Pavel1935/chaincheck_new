import requests
from Constants import Constants
import pytest


class TestMessage:
    def test_message(self, class_tokens):

        url = Constants.API_URL + "/message/send"
        payload = {"topic": "GENERAL",
                   "sender": "John Doe",
                   "email": "johndoe@example.com",
                   "message": "Hello, I have a question about your services.",
                   "recaptcha_token": "SpartakChampion",
                   "recaptcha_version": "v2"
                   }
        try:
            response = requests.post(url, json=payload)
            print("RESPONSE TEXT:", response.text)
        except Exception as e:
            pytest.fail(f"❌ Ошибка при запросе или JSON: {e}")

        data = response.json()
        assert data["ok"] == 1

