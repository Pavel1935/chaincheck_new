import requests
from Constants import Constants
from conftest import class_tokens


class TestHealthCheck:

    def test_health_check(self, class_tokens):

        url = "https://check-dev.g5dl.com/api/v1/health-check"
        refresh_token = class_tokens["refresh_token"]

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
