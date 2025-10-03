import requests
from Constants import Constants
from conftest import report_id
from conftest import class_tokens


class TestAmlShareLink:
    def test_aml_share_link(self, report_id, class_tokens):

        url = Constants.API_URL + "/aml/share/link"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
            "aml_check_id": report_id
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert data["code"]

    def test_aml_share_link_invalid_report_id(self, report_id, class_tokens):

        url = Constants.API_URL + "/aml/share/link"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
            "aml_check_id": '12345-67-spartak-moscow'
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_share_link_without_report_id(self, class_tokens):

        url = Constants.API_URL + "/aml/share/link"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_aml_share_link_invalid_access_token(self, report_id):

        url = Constants.API_URL + "/aml/share/link"

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyODI1OTQ2LCJuYmYiOjE3NTI3Mzk1NDYsImlhdCI6MTc1MjczOTU0NiwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.XFSxiHeRssn28oEY1VEBXi8IhmNF9apI23IXOZxLvF4"}

        payload = {
            "aml_check_id": report_id
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_aml_share_link_without_access_token(self, report_id):

        url = Constants.API_URL + "/aml/share/link"

        payload = {
            "aml_check_id": report_id
        }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_aml_share_link_old_access_token(self, report_id):

        url = Constants.API_URL + "/aml/share/link"

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUzOTcwNDYxLCJuYmYiOjE3NTM4ODQwNjEsImlhdCI6MTc1Mzg4NDA2MSwiZmluZ2VycHJpbnQiOiJYcmt0K2NidVBvYUV5M2xiT3RwRy9YcEJIZzR1ZGQ5QmN1MTExTFFXZU1BPSIsInVzZXJfcm9sZSI6MX0.-LepiYQmzda8HO8400WPyGhYHyguvTiLicBstqqXROQ"}
        payload = {
            "aml_check_id": report_id
        }

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"



