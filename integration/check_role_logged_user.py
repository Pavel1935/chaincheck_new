import pytest
import requests
import jwt
from Constants import Constants
from conftest import get_user_role


class TestCheckRolesLoggedUser:
    """Проверяем роль залогининого пользователя"""

@pytest.mark.parametrize("tokens_by_email,email,expected_role", [
    pytest.param("1@2.io", "1@2.io", 1, id="customer"),  # обычный пользователь
    pytest.param("1@1.io", "1@1.io", 2, id="moderator"),  # модератор
    pytest.param("oukb1147@gmail.com", "oukb1147@gmail.com", 3, id="admin"),  # админ
], indirect=["tokens_by_email"])  # 👈 передаём email внутрь фикстуры
def test_check_role_logged_user(self, tokens_by_email, email, expected_role, db_conn):
    role = get_user_role(db_conn, email)
    print(f"User role from DB for {email}: {role}")

    assert role is not None, f"Пользователь {email} не найден в БД!"
    assert role == expected_role, f"{email}: ожидалась роль {expected_role}, получили {role}"
