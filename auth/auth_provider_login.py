import requests
from Constants import Constants



class TestProviderLogin:

    def test_provider_login(self):

        provider = "google"
        url = f"{Constants.API_URL}/auth/{provider}/login"

        response = requests.get(url)

        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["url"].startswith("https")


    def test_provider_login_incorrect(self):

        provider = "mailru"
        url = f"{Constants.API_URL}/auth/{provider}/login"

        response = requests.get(url)

        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "INVALID_PROVIDER"





