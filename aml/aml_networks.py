import requests
from Constants import Constants
from conftest import tokens


class TestAmlGetNetworks:
    def test_aml_get_networks(self, tokens):

        url = Constants.API_URL + "/aml/networks"

        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["items"]


