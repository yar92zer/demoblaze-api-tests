import allure
import pytest

pytestmark = [pytest.mark.ui, pytest.mark.cart, allure.feature("Корзина UI")]


@pytest.mark.smoke
@allure.title("Добавленный товар появляется в корзине")
def test_added_product_appears_in_cart(
        logged_in_user, home_page, product_page, cart_page
):
    home_page.open()
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    cart_page.open()
    assert "Nexus 6" in cart_page.get_item_titles()


@pytest.mark.regression
@allure.title("Корзина нового пользователя пуста")
def test_new_user_cart_is_empty(logged_in_user, cart_page):
    cart_page.open()
    assert cart_page.is_empty()


@pytest.mark.regression
@allure.title("Итоговая сумма равна сумме цен товаров")
def test_total_equals_sum_of_items(
        logged_in_user, home_page, product_page, cart_page
):
    for title in ("Nexus 6", "Samsung galaxy s6"):
        home_page.open()
        home_page.open_product(title)
        product_page.add_to_cart()
    cart_page.open()
    assert not cart_page.is_empty()
    assert cart_page.get_total() == sum(cart_page.get_item_prices())


@pytest.mark.regression
@allure.title("Оба добавленных товара попадают в корзину")
def test_several_products_in_cart(
        logged_in_user, home_page, product_page, cart_page
):
    expected = {"Nexus 6", "Samsung galaxy s6"}
    for title in expected:
        home_page.open()
        home_page.open_product(title)
        product_page.add_to_cart()
    cart_page.open()
    assert set(cart_page.get_item_titles()) == expected


@pytest.mark.smoke
@allure.title("Удалённый товар пропадает из корзины")
def test_delete_product_from_cart(
        logged_in_user, home_page, product_page, cart_page
):
    home_page.open()
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    cart_page.open()
    cart_page.delete_item("Nexus 6")
    cart_page.open()
    assert "Nexus 6" not in cart_page.get_item_titles()
