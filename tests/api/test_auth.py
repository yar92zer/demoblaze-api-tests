import allure
import pytest

from utils.data_generator import DEFAULT_PASSWORD, unique_username
from utils.encoders import decode_token, encode_password

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


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Логин работает с паролем, закодированным в base64")
def test_login_with_base64_encoded_password(auth):
    username = unique_username()
    password = encode_password(DEFAULT_PASSWORD)

    auth.signup(username, password)
    token = auth.login(username, password)

    assert token
