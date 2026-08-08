import pytest
import allure
from utils.encoders import decode_token

pytestmark = allure.feature("Авторизация")


@pytest.mark.smoke
@pytest.mark.auth
@allure.title("Логин возвращает токен")
def test_login_returns_token(authenticated_user):
    assert authenticated_user["token"]


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Токен обратимо декодируется и содержит логин пользователя")
def test_token_contains_username(authenticated_user):
    decoded = decode_token(authenticated_user["token"])
    assert authenticated_user["username"] in decoded
