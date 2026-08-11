import uuid

from api.models.cart import CartResponse
from api.services.base_service import BaseService
from config.endpoints import Endpoint
from utils.assertions import assert_no_error


class CartService(BaseService):
    def add_to_cart(self, token: str, product_id: int) -> str:
        item_id = str(uuid.uuid4())
        response = self.requester.post(
            Endpoint.ADD_TO_CART,
            payload={"id": item_id, "cookie": token, "prod_id": product_id, "flag": True},
        )
        assert_no_error(response.body)
        return item_id

    def view_cart(self, token: str) -> CartResponse:
        response = self.requester.post(
            Endpoint.VIEW_CART,
            payload={"cookie": token, "flag": True},
        )
        assert_no_error(response.body)
        return CartResponse(**response.body)

    def delete_item(self, item_id: str) -> str:
        response = self.requester.post(
            Endpoint.DELETE_ITEM,
            payload={"id": item_id},
        )
        assert_no_error(response.body)
        return response.body
