import requests
from Constants import Constants
from conftest import report_id


class TestAmlCheckStatus:
    def test_aml_check_status(self, report_id):

        url = Constants.API_URL + "aml/check/status"

        payload = {
          "report_id": report_id
        }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]
