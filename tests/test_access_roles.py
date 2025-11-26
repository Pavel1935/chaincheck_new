import pytest
import requests
import jwt
from Constants import Constants
from conftest import get_user_role


class TestAccessRoles:

    """
    Проверка ролей у пользователей
    """

    @pytest.mark.parametrize(
        "email",
        [
            "pashkarob@gmail.com",  # customer (role=1)
            "1@1.io",  # moderator (role=2)
            "oukb1147@gmail.com",  # admin (role=3)
        ],
        indirect=["email"]
    )
    def test_access_to_reports(self, email, db_conn):

        tokens = email
        access_token = tokens["access_token"]
        login_email = tokens["email"]

        # Запрос к API
        url = Constants.API_URL + "/user/detail"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, json={"email": login_email}, headers=headers)

        data = response.json()
        print(f"\nОтвет API для {login_email}: {data}")

        # Получаем роль напрямую из базы
        role = get_user_role(db_conn, login_email)
        print(f"Роль пользователя в БД: {role}")

        # Логика проверки доступа
        if role in (2, 3):
            print("➡️ Доступ есть (moderator/admin)")
            assert data["ok"] == 1, "API должно разрешить доступ"
            assert data.get("email") == login_email
        else:
            print("⛔ Доступ запрещен (customer)")
            assert data["ok"] == 0, "API должно отказать в доступе"
            assert data.get("error") == "NO_PERMISSION"

    """
    проверяем что можем создать пакет с проверками для пользака
    с разными ролями
    """
    @pytest.mark.parametrize(
        "email",
        [
            "pashkarob@gmail.com",  # customer (role=1)
            "1@1.io",  # moderator (role=2)
            "oukb1147@gmail.com",  # admin (role=3)
        ],
        indirect=["email"])
    def test_package_access_post(self, email):
        url = f"{Constants.API_URL}/package"
        tokens = email
        access_token = tokens["access_token"]
        login_email = tokens["email"]

        payload = {
            "title": "Пакет на удаление",
            "count_checks": 10,
            "price_usd": "1",
            "ref_payout": "0"
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url, headers=headers, json=payload, verify=False)
        data = response.json()
        print(data)

        if email == "pashkarob@gmail.com":
            assert data["ok"] == 0 and data["error"] == "NO_PERMISSION"
        else:
            assert data["ok"] == 1

        """
        проверяем что можем поменять пакет с проверками для пользака
        с разными ролями
        """

    # @pytest.mark.parametrize("tokens_by_email,email", [
    #     pytest.param("pashkarob@gmail.com", "pashkarob@gmail.com", id="customer"),
    #     pytest.param("1@1.io", "1@1.io", id="moderator"),
    #     pytest.param("oukb1147@gmail.com", "oukb1147@gmail.com", id="admin"),
    # ], indirect=["tokens_by_email"])
    # def test_package_access_put(self, tokens_by_email, email):
    #     url = f"{Constants.API_URL}/package"
    #     access_token = tokens_by_email["access_token"]
    #
    #     payload = {
    #         "title": "РазДваТриЗенитушкаСамзнаешь",
    #         "count_checks": 10,
    #         "price_usd": "88",
    #         "ref_payout": "5"
    #     }
    #     headers = {'Authorization': f'Bearer {access_token}'}
    #     response = requests.put(url, headers=headers, json=payload, verify=False)
    #     data = response.json()
    #     print(data)


        """Проверяем роль залогининого пользователя"""
    @pytest.mark.parametrize("tokens_by_email,email,expected_role", [
        pytest.param("1@2.io", "1@2.io", 1, id="customer"),  # обычный пользователь
        pytest.param("1@1.io", "1@1.io", 2, id="moderator"),  # модератор
        pytest.param("oukb1147@gmail.com", "oukb1147@gmail.com", 3, id="admin"),  # админ
    ], indirect=["tokens_by_email"])  # 👈 передаём email внутрь фикстуры
    def test_check_role_logged_user(self, tokens_by_email,email,expected_role, db_conn):

        role = get_user_role(db_conn, email)
        print(f"User role from DB for {email}: {role}")

        assert role is not None, f"Пользователь {email} не найден в БД!"
        assert role == expected_role, f"{email}: ожидалась роль {expected_role}, получили {role}"

    # """Проверка логики доступа"""
        # if role == 1:
        #     # Customer не должен иметь доступ
        #     assert data["ok"] == 0, f"{email}: ожидался отказ доступа, получили {data}"
        #     assert data.get("error") == "NO_PERMISSION", f"{email}: ожидался error=NO_PERMISSION"
        # elif role in (2, 3):
        #     # Moderator и Admin должны иметь доступ
        #     assert data["ok"] == 1, f"{email}: ожидался успех, получили {data}"
        # else:
        #     pytest.fail(f"Неизвестная роль: {role}")
        #
