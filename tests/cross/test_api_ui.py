import allure
import pytest

from utils.encoders import encode_password

pytestmark = [pytest.mark.cross, allure.feature("Сквозные сценарии")]


@pytest.mark.smoke
@allure.title("Товар, добавленный через API, виден в корзине в браузере")
def test_api_added_product_visible_in_ui(
        auth, cart, registered_user, home_page, header, login_modal, cart_page
):
    token = auth.login(
        registered_user["username"], encode_password(registered_user["password"])
    )
    cart.add_to_cart(token, product_id=1)
    home_page.open()
    header.open_login_modal()
    with home_page.page.expect_navigation():
        login_modal.login(registered_user["username"], registered_user["password"])
    cart_page.open()
    assert "Samsung galaxy s6" in cart_page.get_item_titles()


@pytest.mark.regression
@allure.title("Товар, добавленный в браузере, виден в корзине через API")
def test_ui_added_product_visible_in_api(
        auth, cart, registered_user, home_page, header, product_page, logged_in_user
):
    home_page.open()
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    token = auth.login(
        registered_user["username"], encode_password(registered_user["password"])
    )
    body = cart.view_cart(token)
    assert [item.prod_id for item in body.Items] == [3]


@pytest.mark.regression
@allure.title("Цены в каталоге API и на витрине совпадают")
def test_catalog_prices_match_between_api_and_ui(catalog, home_page):
    api_prices = {
        item.title.strip(): item.price for item in catalog.get_entries().Items
    }
    home_page.open()
    ui_titles = home_page.get_product_titles()
    ui_prices = home_page.get_product_prices()
    for title, raw_price in zip(ui_titles, ui_prices):
        assert float(raw_price.lstrip("$")) == api_prices[title]
