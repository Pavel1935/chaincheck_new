import requests
from Constants import Constants
from conftest import class_tokens


class TestPackageList:
    def test_package_list(self, class_tokens):

        url = Constants.API_URL + "/package/list"
        access_token = class_tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()

        assert data["ok"] == 1
        assert "items" in data

    def test_package_list_without_token(self):

        url = Constants.API_URL + "/package/list"


        response = requests.get(url)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] in "UNAUTHORIZED"

    def test_package_old_token(self):
        url = Constants.API_URL + "/package/list"

        headers = {'Authorization': 'Bearer ' + "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NzE5NzAwLCJuYmYiOjE3NTQ2MzMzMDAsImlhdCI6MTc1NDYzMzMwMCwiZmluZ2VycHJpbnQiOiJJTTA4Z1NyK3FhbnJDVkhMc2FnV1RBbnoxVlZ4NFVTVmxibDBnT2M2cldNPSIsInVzZXJfcm9sZSI6M30.RKlEY_ - J9eo7WwUyMcfLVxEv14NWkuH2k3vi1Pz2tio"}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] in "UNAUTHORIZED"

    def test_package_incorrect_token(self):
        url = Constants.API_URL + "/package/list"

        headers = {'Authorization': 'Bearer ' + "hiJohneeyJhbiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzU0NzE4ODc1LCJuYmYiOjE3NTQ2MzI0NzUsImlhdCI6MTc1NDYzMjQ3NSwiZmluZ2VycHJpbnQiOiJJTTA4Z1NyK3FhbnJDVkhMc2FnV1RBbnoxVlZ4NFVTVmxibDBnT2M2cldNPSIsInVzZXJfcm9sZSI6M30.qYdvrwTC3yPHhGBXtAYxQIVdV0CgNAt5gacI13f1rS0"}

        response = requests.get(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] in "UNAUTHORIZED"

