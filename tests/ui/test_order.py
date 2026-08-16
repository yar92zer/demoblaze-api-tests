import allure
import pytest
from utils.data_generator import order_data

pytestmark = [pytest.mark.ui, allure.feature("Оформление заказа")]


@pytest.mark.smoke
@allure.title("Заказ оформляется и показывает подтверждение")
def test_purchase_shows_confirmation(
        logged_in_user, home_page, product_page, cart_page, order_modal
):
    home_page.open()
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    cart_page.open()
    cart_page.place_order()
    order_modal.wait_opened()
    order = order_data()
    order_modal.fill_order(order)
    order_modal.purchase()
    assert order_modal.get_confirmation_title() == "Thank you for your purchase!"


@pytest.mark.negative
@allure.title("Постая форма заказа отклоняется")
def test_purchase_with_empty_form_rejected(
        logged_in_user, home_page, product_page, cart_page, order_modal):
    home_page.open()
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    cart_page.open()
    cart_page.place_order()
    order_modal.wait_opened()
    message = order_modal.purchase_expecting_alert()
    assert message == "Please fill out Name and Creditcard."


@pytest.mark.regression
@allure.title("Подтверждение сдержит имя, карут и сумму заказа")
def test_confirmation_contains_order_details(
        logged_in_user, home_page, product_page, cart_page, order_modal,
):
    home_page.open()
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    cart_page.open()
    total = cart_page.get_total()
    cart_page.place_order()
    order = order_data()
    order_modal.wait_opened()
    order_modal.fill_order(order)
    order_modal.purchase()
    details = order_modal.get_confirmation_text()
    assert order["name"] in details
    assert order["card"] in details
    assert str(total) in details
