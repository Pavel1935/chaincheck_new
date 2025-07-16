import requests
from Constants import Constants


class TestPackageDelete:
    def test_package_delete(self):
        package_id = "095a5476-2e17-4677-a91b-06be1e336949"
        url = Constants.API_URL + "/package/" + package_id

        payload = {
        }

        headers = {'Authorization': 'Bearer ' + Constants.TOKEN}

        response = requests.delete(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
