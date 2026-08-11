import allure
import pytest

from utils.assertions import assert_no_error

pytestmark = allure.feature("Корзина")


@pytest.mark.smoke
@pytest.mark.cart
@allure.title("Добавленный товар появляется в корзине")
def test_added_product_appears_in_cart(cart, cart_with_product):
    body = cart.view_cart(cart_with_product["token"])
    assert_no_error(body)
    ids = [item.id for item in body.Items]
    assert cart_with_product["item_id"] in ids


@pytest.mark.cart
@pytest.mark.regression
@allure.title("Корзина нового пользователя пуста")
def test_new_user_cart_is_empty(cart, authenticated_user):
    body = cart.view_cart(authenticated_user["token"])
    assert_no_error(body)
    assert body.Items == []


@pytest.mark.cart
@pytest.mark.negative
@allure.title("Некорректный токен возвращает ошибку в теле ответа")
def test_malformed_token_returns_error(cart):
    with pytest.raises(AssertionError, match="token malformed"):
        cart.view_cart("definitely-not-a-token")
