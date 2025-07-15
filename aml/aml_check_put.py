import requests
from Constants import Constants
from conftest import report_id



class TestAmlCheckPut:
    def test_aml_check_put(self, report_id):

        url = Constants.API_URL + "aml/check"

        payload = {
          "report_id": report_id,
          "title": "Проверь адрес"
        }
        headers = {'Authorization': 'Bearer ' + Constants.TOKEN,
                   'Cookie': Constants.REFRESH_TOKEN
                   }

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1
