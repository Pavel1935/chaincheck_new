import requests
from Constants import Constants


class TestPackageList:
    def test_package_list(self):

        url = Constants.API_URL + "/package/list"


        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert "items" in data
