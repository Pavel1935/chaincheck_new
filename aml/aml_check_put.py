import requests
from Constants import Constants
from conftest import report_id
from conftest import class_tokens



class TestAmlCheckPut:
    def test_aml_check_put(self, class_tokens):

        url = Constants.API_URL + "aml/check"
        access_token = class_tokens["access_token"]

        payload = {
          "report_id": "65cb79b3-72a6-42a3-af67-9a528b70cd15",
          "title": "Проверь БЫСТРО адрес"
        }
        headers = {'Authorization': 'Bearer ' + access_token
                   }

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["id"]

    def test_aml_check_put_without_title(self, class_tokens):

        url = Constants.API_URL + "aml/check"
        access_token = class_tokens["access_token"]

        payload = {
          "report_id": "65cb79b3-72a6-42a3-af67-9a528b70cd15"
        }
        headers = {'Authorization': 'Bearer ' + access_token
                   }

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
        assert data["result"]["id"]

    def test_aml_check_put_without_report_id(self, class_tokens):

        url = Constants.API_URL + "aml/check"
        access_token = class_tokens["access_token"]

        payload = {
          "title": "Проверь БЫСТРО адрес"
        }
        headers = {'Authorization': 'Bearer ' + access_token
                   }

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_check_put_invalid_report_id(self, class_tokens):

        url = Constants.API_URL + "aml/check"
        access_token = class_tokens["access_token"]

        payload = {
            "report_id": "65cb79refgqwegb3-72a6-42a3-af67-9a528b70cd15",
            "title": "Проверь БЫСТРО адрес"
        }

        headers = {'Authorization': 'Bearer ' + access_token
                   }

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_UUID"

