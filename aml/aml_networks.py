import requests
from Constants import Constants
from conftest import report_id


class TestAmlGetNetworks:
    def test_aml_get_networks(self):

        url = Constants.API_URL + "/aml/networks"

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["items"]

