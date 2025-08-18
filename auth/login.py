import requests
from Constants import Constants


class TestLogin:

    def test_login(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "oukb1147@gmail.com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_login_without_dog(self):
        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "support-team@company_name.net"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_login_without_space(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "support-team@company name.net"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_login_without_dog_and_domen(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "user+tagexample.com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_login_without_incorrect_domen(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "12345user@mail-provider_com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_login_without(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "name@domain@domain.net"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_login_domen_shorter_than_two_characters(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "user@mail.c"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"

    def test_login_domen_two_point(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "user@mail..io"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"

    def test_login_domen_invalid_domen_name(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "user@-domain.com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"

    def test_login_domen_invalid_domen2_name(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "-user@domain.com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"

    def test_login_domen_inсorrect_domen(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "tests@m_ail.ru"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"


    def test_login_domen_two_point_name(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "te..st@mail.ru"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"

    def test_login_with_plus(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "tests@m+ail.ru"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_EMAIL"

    def test_login_with_quote(self):

        url = Constants.API_URL + "/auth/login"

        payload = {
              "email": "tests'io'domain.com"
            }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

    def test_login_with_point_and_space(self):
        url = Constants.API_URL + "/auth/login"

        payload = {
            "email": ".tests... iotoday@domain.com"
        }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "BAD_REQUEST"

