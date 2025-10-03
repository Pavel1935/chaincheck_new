import requests
from Constants import Constants
from conftest import class_tokens


class TestAmlGetNetworks:
    def test_aml_get_networks(self, class_tokens):

        url = Constants.API_URL + "/aml/networks"

        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["items"]


