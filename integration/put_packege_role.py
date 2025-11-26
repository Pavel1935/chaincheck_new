import pytest
import requests
import jwt
from Constants import Constants
from conftest import get_user_role
import pytest
import requests
from psycopg2.extras import RealDictCursor
from Constants import Constants


class TestPutPackegeRole:

    """Customer (role=1) не может ИЗМЕНЯТЬ пакет: API даёт NO_PERMISSION, роль в БД = 1."""

    @pytest.mark.parametrize(
        "email",
        [
            "pashkarob@gmail.com",  # customer (role=1)
            "1@1.io",  # moderator (role=2)
            "oukb1147@gmail.com",  # admin (role=3)
        ],
        indirect=["email"])
    def test_put_package(self, email, db_conn):
        tokens = email
        access_token = tokens["access_token"]
        login_email = tokens["email"]

        # Получаем роль напрямую из базы
        role = get_user_role(db_conn, login_email)
        print(f"Роль пользователя в БД: {role}")


        # Проверяем, что существует пакет нужный нам
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, title, status
                FROM packages
                WHERE title = %s AND status = 0
                ORDER BY created_at DESC NULLS LAST, id DESC
                LIMIT 1
                """,
                ("Спартак Москва",),
            )
            row = cur.fetchone()
        assert row, "Пакет не найден в БД после создания"
        package_id = row["id"]
        print(f"В базе данных после создания: id={package_id}, status={row['status']}")
        assert row["status"] == 0  # создан, но не оплачен

        url = f"{Constants.API_URL}/package"

        payload = {
              "id": package_id,
              "title": "Торпедо",
              "price_usd": "11",
              "count_checks": 2,
              "ref_payout": "1",
              "status": 0
            }
        headers = {'Authorization': 'Bearer ' + access_token}

        response = requests.put(url, headers=headers, json=payload)
        print("RESPONSE TEXT:", response.text)
        data = response.json()
        assert data["ok"] == 1

