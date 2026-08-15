import allure
import pytest

from utils.data_generator import unique_username, DEFAULT_PASSWORD

pytestmark = [pytest.mark.ui, pytest.mark.auth, allure.feature("Авторизация UI")]


@pytest.mark.smoke
@allure.title("Регистрация нового пользователя через форму")
def test_signup_new_user(home_page, header, signup_modal):
    home_page.open()
    header.open_signup_modal()
    message = signup_modal.register(unique_username(), DEFAULT_PASSWORD)
    assert message == "Sign up successful."


@pytest.mark.regression
@allure.title("Повторная регистрация занятого логина отклоняется")
def test_signup_existing_user(home_page, header, signup_modal, registered_user):
    home_page.open()
    header.open_signup_modal()
    message = signup_modal.register(
        registered_user["username"], registered_user["password"]
    )
    assert message == "This user already exist."


@pytest.mark.smoke
@allure.title("Вход показывает имя пользователя в шапке")
def test_login_shows_username(home_page, header, login_modal, registered_user):
    home_page.open()
    header.open_login_modal()
    login_modal.login(registered_user["username"], registered_user["password"])
    assert header.get_logged_user() == registered_user["username"]


@pytest.mark.regression
@allure.title("Выход возвращает шапку в состояние гостя")
def test_logout_returns_to_guest(home_page, header, login_modal, registered_user):
    home_page.open()
    header.open_login_modal()
    login_modal.login(registered_user["username"], registered_user["password"])
    header.logout()
    assert not header.is_logged_in()


@pytest.mark.negative
@allure.title("Вход с неверным паролем отклоняется")
def test_login_wrong_password(home_page, header, login_modal, registered_user):
    home_page.open()
    header.open_login_modal()
    message = login_modal.login_expecting_alert(
        registered_user["username"], "definitely_wrong"
    )
    assert message == "Wrong password."


@pytest.mark.negative
@allure.title("Вход несуществующего пользователя отклоняется")
def test_login_unknown_user(home_page, header, login_modal):
    home_page.open()
    header.open_login_modal()
    message = login_modal.login_expecting_alert(unique_username(), DEFAULT_PASSWORD)
    assert message == "User does not exist."
