import requests
from Constants import Constants
from conftest import report_id


class TestAmlShareLink:
    def test_aml_share_link(self, report_id):

        url = Constants.API_URL + "/aml/share/link"

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        payload = {
            "aml_check_id": report_id
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["code"]

