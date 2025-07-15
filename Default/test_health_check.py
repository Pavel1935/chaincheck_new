import requests
from Constants import Constants


class TestHealthCheck:

    def test_health_check(self):

        response = requests.get(Constants.API_URL + "health-check")
        print("RESPONSE TEXT:", response.text)

        assert response.status_code == 200

        data = response.json()

        assert data["ok"] == 1
        assert data["status"].startswith("Api is ready. Server time is ")
