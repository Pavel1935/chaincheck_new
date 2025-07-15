import requests
from Constants import Constants
from conftest import report_id


class TestAmlCheckHistoryLimit:
    def test_aml_check_history_limit(self):

        url = Constants.API_URL + "/aml/check/history"

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}
        params = "limit=0"

        response = requests.get(url, headers=headers, params=params)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["result"]["items"]

