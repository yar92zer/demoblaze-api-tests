import allure
import pytest

from client.endpoints import Endpoint

pytestmark = [pytest.mark.regression,
              allure.feature("Известные дефекты стенда")
              ]


@pytest.mark.negative
@pytest.mark.xfail(
    reason="Дефект /deleteitem не требует токена, позиция удаляется по одному id",
    strict=True,
)
@allure.title("Позицию корзины нельзя удалить без токена валадельца")
def test_cart_item_cannot_be_deleted_without_owner_token(cart, authenticated_user):
    item_id = cart.add_to_cart(authenticated_user["token"], product_id=1)
    with pytest.raises(AssertionError):
        cart.delete_item(item_id)
    assert cart.view_cart(authenticated_user["token"]).Items


@pytest.mark.negative
@pytest.mark.xfail(
    reason="Дефект нечисловой id валит бэкенд с 500 и HTML вместо JSON",
    strict=True,
)
@allure.title("Нечисловой id не должен валить бэкенд")
def test_view_with_non_numeric_id_does_not_crash(requester):
    response = requester.post(Endpoint.VIEW, payload={"id": "abc"})
    assert response.status == 200
