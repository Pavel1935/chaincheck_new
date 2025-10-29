import pytest
import requests
from psycopg2.extras import RealDictCursor
from Constants import Constants


class TestIntegration:
    """Тест который создает юзера, проверяет его наличие в БД, удаляет
    и проверяет что статус его изменился на 2 (удален)"""

    def test_create_user_check_bd_delete(self, tokens_by_email, db_conn):
        login = tokens_by_email  # фикстура возвращает функцию
        tokens = login("oukb1147@gmail.com")
        access_token = tokens["access_token"]

        url = Constants.API_URL + "/package"

        payload = {
              "title": "Спартак Москва",
              "count_checks": 100,
              "price_usd": "10",
              "ref_payout": "1000"
            }

        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print("CREATE RESPONSE:", data)

        # Проверяем, что пакет появился в БД
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

        # удаляем пакет
        delete_url = Constants.API_URL + "/package/" + package_id
        delete_payload = {
        }

        delete_response = requests.delete(delete_url, headers=headers, json=delete_payload)
        print("RESPONSE TEXT:", delete_response.text)

        # проверяем что у пакета статус 2
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, status
                FROM packages
                WHERE id = %s AND status = 2
                """,
                (package_id,),
            )
            row = cur.fetchone()
        assert row, "Пакет не найден в БД после удаления"
        print(f"В базе данных после удаления: id={package_id}, status={row['status']}")
        assert row["status"] == 2  # пакет удален

    """Customer (role=1) не может создавать пакет: API даёт NO_PERMISSION, роль в БД = 1."""

    def test_create_customer_role_1(self, tokens_by_email, db_conn):
        email = "1@2.io"
        login = tokens_by_email  # фикстура возвращает функцию
        tokens = login(email)
        access_token = tokens["access_token"]

        url = Constants.API_URL + "/package"

        payload = {
            "title": "Москва",
            "count_checks": 20,
            "price_usd": "2",
            "ref_payout": "2"
        }

        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.post(url, headers=headers, json=payload)

        data = response.json()
        print("CREATE RESPONSE:", data)

        assert data["ok"] == 0 and data["error"] == "NO_PERMISSION"

        # Проверяем, что пакет появился в БД
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT email, role
                FROM users
                WHERE email = %s
                """,
                (email,),
            )
            row = cur.fetchone()
        assert row, "Пользователь не найден в БД после создания"
        email = row['email']
        print(f"В базе данных после создания: email={email}, role={row['role']}")
        assert row["role"] == 1 and row["email"] == email



