import requests
from Constants import Constants


class TestHealthCheck:

    def test_health_check(self):

        url = Constants.API_URL + "/aml/share/link"

        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        assert response.status_code == 200

        data = response.json()

        assert data["ok"] == 1
        assert data["status"].startswith("Api is ready. Server time is ")
