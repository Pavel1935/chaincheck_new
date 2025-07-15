import requests
from Constants import Constants
from conftest import report_id


class TestAmlShareLinkCode:
    def test_aml_share_link_code(self):

        url = Constants.API_URL + "/aml/share/link"

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}
        params = "code=0952455167"

        response = requests.get(url, headers=headers, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["id"]
        assert data["title"]


