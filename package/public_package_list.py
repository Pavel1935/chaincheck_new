import requests
from Constants import Constants



class TestPackageList:
    def test_package_list(self):

        url = Constants.API_URL + "/public/package/list"

        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert "result" in data
