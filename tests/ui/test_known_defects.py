import allure
import pytest

pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression,
    allure.feature("Известные дефекты стенда"),
]


@pytest.mark.xfail(
    reason="Дефект гость получает 'Product added', авторизованный - с точкой",
    strict=True,
)
@allure.title("Текст подтверждения одинаков для гостя и авторизованного")
def test_add_to_cart_alert_is_consistent(
        home_page, product_page, header, login_modal, registered_user
):
    home_page.open()
    home_page.open_product("Nexus 6")
    guest_message = product_page.add_to_cart()

    home_page.open()
    header.open_login_modal()
    with home_page.page.expect_navigation():
        login_modal.login(registered_user["username"], registered_user["password"])

    home_page.open()
    home_page.open_product("Nexus 6")
    user_message = product_page.add_to_cart()

    assert guest_message == user_message
