import requests
from Constants import Constants
from conftest import class_tokens


class TestPackageDelete:
    def test_package_delete(self, tokens):

        package_id = "c99fdb3e-6d9d-4cca-9adb-a016fb5c50bb"
        url = Constants.API_URL + "/package/" + package_id
        access_token = tokens["access_token"]

        payload = {
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.delete(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_package_delete_invalid_id(self, class_tokens):

        package_id = "Москва"
        url = Constants.API_URL + "/package/" + package_id
        access_token = class_tokens["access_token"]

        payload = {
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.delete(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_package_delete_incorrect_id(self, class_tokens):

        package_id = "72bf6fFDG0f-7bb5-46bc-8e91-b7ff6e4bc663"
        url = Constants.API_URL + "/package/" + package_id
        access_token = class_tokens["access_token"]

        payload = {
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.delete(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"


    def test_package_delete_without_access_token(self):

        package_id = "72bf6f0f-7bb5-46bc-8e91-b7ff6e4bc663"
        url = Constants.API_URL + "/package/" + package_id

        payload = {
        }

        response = requests.delete(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"

    def test_package_delete_old_access_token(self):

        package_id = "72bf6f0f-7bb5-46bc-8e91-b7ff6e4bc663"
        url = Constants.API_URL + "/package/" + package_id

        payload = {
        }

        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUxOTg5NTM4LCJuYmYiOjE3NTE5MDMxMzgsImlhdCI6MTc1MTkwMzEzOCwiZmluZ2VycHJpbnQiOiJsR0xneGE2Yi9ieEhUVHVJTzlPKzdseUVrZnlmNnNQbC9EUXgxWCt6bWdvPSIsInVzZXJfcm9sZSI6M30.nMXEkTRqVial-Uz_2_OvrtVrHKrKxNLjgAqM128Oh4g"}

        response = requests.delete(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "UNAUTHORIZED"
