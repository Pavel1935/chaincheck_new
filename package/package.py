import requests
from Constants import Constants
from conftest import tokens


class TestPackage:
    def test_package(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "10",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_package_big_price(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_package_empty_title(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "",
              "count_checks": 100,
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_package_without_payload(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_package_without_title(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "count_checks": 100,
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"


    def test_package_without_count_checks(self, tokens):


        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert response.json()["ok"] == 0
        assert data["error"] == "BAD_REQUEST"


    def test_package_without_price(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

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

    def test_package_without_ref(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "2",
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_package_lots_of_characters_title(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
            "title": "dskjfbkjvb;ksjvb;akdjfbvdakjbvadkjbvkajdvkjdavajdhfvjadhv;kjdbhv;kjadhv;kjadv;kjadv;kjadvndsvkd;bjhd;jlrghe;jgrh;ejgh;jkeghkjgegh;jkwehg;kjheg;jheg;kjherg;kjhe;kgjh;ekrgh;kwrjhg;wrkthjwlrjhwlrjhwlrjhlwejhgwehgnjhqe;jhqefkbhvdsk;jhbskdjbksjdnbsjnb,sdnb/sfdnb/sfndbsdnfbv;jhds;kjhds;kghwcuhwnlhhgerwhjhgerjj",
            "count_checks": 100,
            "price_usd": "2",
            "ref_payout": "100"
        }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "VALIDATION_TITLE_INVALID"

    def test_package(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_package(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_package(self, tokens):

        url = Constants.API_URL + "/package"
        access_token = tokens["access_token"]

        payload = {
              "title": "ВпередНашСпартакМосква",
              "count_checks": 100,
              "price_usd": "2",
              "ref_payout": "100"
            }

        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.post(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

