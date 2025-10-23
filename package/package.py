import pytest
import requests
from Constants import Constants
from conftest import tokens


@pytest.mark.usefixtures("class_tokens")
class TestPackage:

    def test_package(self, class_tokens):

        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
              "title": "Спартак Москва",
              "count_checks": 100,
              "price_usd": "10",
              "ref_payout": "1000"
            }

        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.parametrize(
        "data, value",
        [
            ("title", "в"),
            ("title", "привет"),
            ("title", "!:,.;/"),
            ("title", "123")
        ])
    def test_package_positive_title(self, class_tokens, data, value):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            data: value,
            "count_checks": 100,
            "price_usd": "10",
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.parametrize(
        "data_1, value_1",
        [
            ("count_checks", 1),
            ("count_checks", 50),
            ("count_checks", 500),
            ("count_checks", 1000000)
        ])
    def test_package_positive_count_checks(self, class_tokens, data_1, value_1):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            "title": "ВпередНашСпартакМосква",
            data_1: value_1,
            "price_usd": "10",
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.parametrize(
        "data_2, value_2",
        [
            ("price_usd", "0.01"),
            ("price_usd", "1"),
            ("price_usd", "50"),
            ("price_usd", "500"),
            ("price_usd", "1000000")
        ])
    def test_package_positive_price_usd(self, class_tokens, data_2, value_2):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            "title": "ВпередНашСпартакМосква",
            "count_checks": 100,
            data_2: value_2,
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.parametrize(
        "data_3, value_3",
        [
            ("ref_payout", "0.01"),
            ("ref_payout", "1"),
            ("ref_payout", "50.5"),
            ("ref_payout", "100"),
            ("ref_payout", "999")
        ])
    def test_package_positive_ref_payout(self, class_tokens, data_3, value_3):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            "title": "ВпередНашСпартакМосква",
            "count_checks": 100,
            "price_usd": "10",
            data_3: value_3
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    @pytest.mark.parametrize(
        "data_4, value_4",
        [
            ("title", ""),
            ("title", "dskjfbkjvb;ksjvb;akdjfbvdakjbvadkjbvkajdvkjdavajdhfvjadhv;kjdbhv;kjadhv;kjadv;kjadv;kjadvndsvkd;bjhd;jlrghe;jgrh;ejgh;jkeghkjgegh;jkwehg;kjheg;jheg;kjherg;kjhe;kgjh;ekrgh;kwrjhg;wrkthjwlrjhwlrjhwlrjhlwejhgwehgnjhqe;jhqefkbhvdsk;jhbskdjbksjdnbsjnb,sdnb/sfdnb/sfndbsdnfbv;jhds;kjhds;kghwcuhwnlhhgerwhjhgerjj")
        ])
    def test_package_negative_title(self, class_tokens, data_4, value_4):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            data_4: value_4,
            "count_checks": 100,
            "price_usd": "10",
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "VALIDATION_TITLE"

    @pytest.mark.parametrize(
        "data_5, value_5",
        [
            ("count_checks", "привет"),
            ("count_checks", -1),
            ("count_checks", 1.1),
            ("", 10)


        ])
    def test_package_negative_count_checks(self, class_tokens, data_5, value_5):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            "title": "ВпередНашСпартакМосква",
            data_5: value_5,
            "price_usd": "10",
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    @pytest.mark.parametrize(
        "data_6, value_6",
        [
            ("price_usd", "0,01"),
            ("price_usd", "-1"),
            ("price_usd", "0"),
            ("price_usd", ""),
            ("price_usd", "1000001"),
            ("price_usd", "hi"),
            ("price_usd", "$%^&&*$%"),
            ("", "10000")
        ])
    def test_package_negative_price_usd(self, class_tokens, data_6, value_6):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            "title": "ВпередНашСпартакМосква",
            "count_checks": 100,
            data_6: value_6,
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST" or "VALIDATION_TITLE"

    @pytest.mark.parametrize(
        "data_7, value_7",
        [
            ("ref_payout", "0,01"),
            ("ref_payout", "-1"),
            ("ref_payout", ""),
            ("ref_payout", "10001"),
            ("ref_payout", "hi"),
            ("ref_payout", "$%^&&*$%"),
            ("", "10000")
        ])
    def test_package_negative_ref_payout(self, class_tokens, data_7, value_7):
        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
            "title": "ВпередНашСпартакМосква",
            "count_checks": 100,
            "price_usd": "10",
            data_7: value_7
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST" or "VALIDATION_TITLE"

    def test_package_without_title(self, class_tokens):

        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
              "count_checks": 100,
              "price_usd": "10",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_package_without_count_checks(self, class_tokens):

        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "price_usd": "10",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_package_without_price_usd(self, class_tokens):

        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_package_without_ref_payout(self, class_tokens):

        url = Constants.API_URL + "/package"
        access_token = class_tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "10"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"
