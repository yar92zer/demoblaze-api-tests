import allure
import pytest

from utils.data_generator import DEFAULT_PASSWORD, unique_username
from utils.encoders import decode_token, encode_password

pytestmark = allure.feature("Авторизация")


@pytest.mark.smoke
@pytest.mark.auth
@allure.title("Регистрация и вход возвращают рабочий токен")
def test_signup_and_login(auth):
    username = unique_username()
    auth.signup(username, DEFAULT_PASSWORD)
    token = auth.login(username, DEFAULT_PASSWORD)
    assert username in decode_token(token)


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Токен обратимо декодируется и содержит логин пользователя")
def test_token_is_reversible(authenticated_user):
    decoded = decode_token(authenticated_user["token"])
    username = authenticated_user["username"]
    assert decoded.startswith(username)
    assert decoded[len(username):].isdigit()


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Логин работает с паролем, закодированным в base64")
def test_login_with_base64_encoded_password(auth):
    username = unique_username()
    password = encode_password(DEFAULT_PASSWORD)
    auth.signup(username, password)
    token = auth.login(username, password)
    assert username in decode_token(token)


@pytest.mark.auth
@pytest.mark.negative
@allure.title("Вход с неверным паролем отклоняется")
def test_login_with_wrong_password(auth):
    username = unique_username()
    auth.signup(username, DEFAULT_PASSWORD)
    with pytest.raises(AssertionError):
        auth.login(username, "wrong_password")
