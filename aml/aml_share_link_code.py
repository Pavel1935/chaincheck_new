import requests
from Constants import Constants


class TestAmlShareLinkCode:

    def test_aml_share_link_code(self):

        url = Constants.API_URL + "/aml/share/link"

        params = "code=123456"

        response = requests.get(url, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        # assert data["id"]
        # assert data["title"]

    def test_aml_share_without_link_code(self):

        url = Constants.API_URL + "/aml/share/link"

        params = "code="

        response = requests.get(url, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_share_invalid_link_code(self):

        url = Constants.API_URL + "/aml/share/link"

        params = "code=1434spartak229737"

        response = requests.get(url, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "ENTITY_NOT_FOUND"

    def test_aml_share_without_param_link_code(self):

        url = Constants.API_URL + "/aml/share/link"

        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_share_link_code_invalid_param(self):

        url = Constants.API_URL + "/aml/share/link"

        params = "=1434229737"

        response = requests.get(url, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_share_link_code_without_data_param(self):

        url = Constants.API_URL + "/aml/share/link"

        params = ""

        response = requests.get(url, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"






