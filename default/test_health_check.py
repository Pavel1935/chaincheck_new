import requests
from Constants import Constants
from conftest import tokens


class TestHealthCheck:

    def test_health_check(self, tokens):

        url = "https://check-dev.g5dl.com/api/v1/health-check"
        refresh_token = tokens["refresh_token"]

        payload = {}
        headers = {
            'Cookie': f'refresh_token={refresh_token}'
        }

        response = requests.get(url, headers=headers, data=payload)
        print("RESPONSE TEXT:", response.text)

        assert response.status_code == 200

        data = response.json()

        assert data["ok"] == 1
        assert data["status"].startswith("Api is ready. Server time is ")
