import pytest


@pytest.mark.smoke
@pytest.mark.cart
def test_added_product_appears_in_cart(cart, cart_with_product):
    body = cart.view_cart(cart_with_product["token"])
    ids = [item["id"] for item in body["Items"]]
    assert cart_with_product["item_id"] in ids


@pytest.mark.cart
@pytest.mark.regression
def test_new_user_cart_is_empty(cart, authenticated_user):
    body = cart.view_cart(authenticated_user["token"])
    assert body["Items"] == []


@pytest.mark.cart
@pytest.mark.negative
def test_malformed_token_returns_error(cart):
    body = cart.view_cart("definitely-not-a-token")
    assert "errorMessage" in body
