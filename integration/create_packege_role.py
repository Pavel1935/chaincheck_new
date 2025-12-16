import pytest
import requests
import jwt
from Constants import Constants
from conftest import get_user_role


class TestCreatePackegeRole:

    """Невозможно купить пакет неавторизованному пользователю"""
    def test_guest_cannot_buy_package(self):
        url = f"{Constants.API_URL}/package"

        payload = {
            "title": "Пакет по ролям",
            "count_checks": 10,
            "price_usd": "1",
            "ref_payout": "0"
        }
        headers = {'Authorization': f''}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print("RESPONSE TEXT:", response.text)

    """Создание пакета доступно только пользователям с ролями moderator и admin"""

    @pytest.mark.parametrize(
        "email",
        [
            "pashkarob@gmail.com",  # customer (role=1)
            "1@1.io",  # moderator (role=2)
            "oukb1147@gmail.com",  # admin (role=3)
        ],
        indirect=["email"])
    def test_access_create_package(self, email, db_conn):
        url = f"{Constants.API_URL}/package"

        tokens = email
        access_token = tokens["access_token"]
        login_email = tokens["email"]

        payload = {
            "title": "Пакет по ролям",
            "count_checks": 1488,
            "price_usd": "1488",
            "ref_payout": "1"
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url, headers=headers, json=payload, verify=False)
        data = response.json()
        print("RESPONSE TEXT:", response.text)

        print(f"\nОтвет API для {login_email}: {data}")

        # Получаем роль напрямую из базы
        role = get_user_role(db_conn, login_email)
        print(f"Роль пользователя в БД: {role}")

        if role in (2, 3):
            print("➡️ Пакет создан (moderator/admin)")
            assert data["ok"] == 1, "Должен создаться пакет"
        else:
            print("➡️ Пакет не создан (customer)")
            assert data["ok"] == 0, "Покет не создается так как у пользователя нет прав"
            assert data["error"] == 'NO_PERMISSION'

    """Ошибка при покупке у пользователей есдли отсутствует аксесс токен"""

    @pytest.mark.parametrize(
        "email",
        [
            "pashkarob@gmail.com",  # customer (role=1)
            "1@1.io",  # moderator (role=2)
            "oukb1147@gmail.com",  # admin (role=3)
        ],
        indirect=["email"])
    def test_create_package_without_access_token(self, email, db_conn):
        url = f"{Constants.API_URL}/package"

        tokens = email
        # access_token = tokens["access_token"]
        login_email = tokens["email"]

        payload = {
            "title": "Пакет по ролям",
            "count_checks": 10,
            "price_usd": "1",
            "ref_payout": "0"
        }
        headers = {'Authorization': f''}
        response = requests.post(url, headers=headers, json=payload, verify=False)
        data = response.json()
        print("RESPONSE TEXT:", response.text)

        print(f"\nОтвет API для {login_email}: {data}")

        # Получаем роль напрямую из базы
        role = get_user_role(db_conn, login_email)
        print(f"Роль пользователя в БД: {role}")

        assert data["ok"] == 0, "Не должен создаться пакет"
        assert data.get("error") == "UNAUTHORIZED"

    """Ошибка при покупке у пользователей с невалидным аксесс токеном"""

    @pytest.mark.parametrize(
        "email",
        [
            "pashkarob@gmail.com",  # customer (role=1)
            "1@1.io",  # moderator (role=2)
            "oukb1147@gmail.com",  # admin (role=3)
        ],
        indirect=["email"])
    def test_create_package_without_access_token(self, email, db_conn):
        url = f"{Constants.API_URL}/package"

        tokens = email
        # access_token = tokens["access_token"]
        login_email = tokens["email"]

        payload = {
            "title": "Пакет по ролям",
            "count_checks": 10,
            "price_usd": "1",
            "ref_payout": "0"
        }
        headers = {'Authorization': f'jbgjljhhjhjfghv7jhfklj'}
        response = requests.post(url, headers=headers, json=payload, verify=False)
        data = response.json()
        print("RESPONSE TEXT:", response.text)

        print(f"\nОтвет API для {login_email}: {data}")

        # Получаем роль напрямую из базы
        role = get_user_role(db_conn, login_email)
        print(f"Роль пользователя в БД: {role}")

        assert data["ok"] == 0, "Не должен создаться пакет"
        assert data.get("error") == "UNAUTHORIZED"


