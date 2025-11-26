import pytest
import requests
import jwt
from Constants import Constants
from conftest import get_user_role


class TestUserDetailRoles:

    """
    Проверка что НЕ ВСЕ роли юзеров могут просматривать детали у пользователей
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
def test_access_to_user_detail(self, email, db_conn):

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
