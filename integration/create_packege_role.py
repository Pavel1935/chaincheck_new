import pytest
import requests
import jwt
from Constants import Constants
from conftest import get_user_role


class TestCreatePackegeRole:

    """Customer (role=1) не может создавать пакет: API даёт NO_PERMISSION, роль в БД = 1."""

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
            "count_checks": 10,
            "price_usd": "1",
            "ref_payout": "0"
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url, headers=headers, json=payload, verify=False)
        data = response.json()
        print("RESPONSE TEXT:", response.text)

        print(f"\nОтвет API для {login_email}: {data}")

        # Получаем роль напрямую из базы
        role = get_user_role(db_conn, login_email)
        print(f"Роль пользователя в БД: {role}")

        # Логика проверки доступа
        if role in (2, 3):
            print("➡️ Пакет создан (moderator/admin)")
            assert data["ok"] == 1, "Должен создаться пакет"
            # assert data.get("email") == login_email
        else:
            print("⛔ Пакет не создан (customer)")
            assert data["ok"] == 0, "Пакет не создасться"
            assert data.get("error") == "NO_PERMISSION"