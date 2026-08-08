import uuid

from api.models.cart import CartResponse
from api.services.base_service import BaseService
from config.endpoints import Endpoint


class CartService(BaseService):
    def add_to_cart(self, token: str, product_id: int) -> str:
        item_id = str(uuid.uuid4())
        self.requester.post(
            Endpoint.ADD_TO_CART,
            payload={
                "id": item_id,
                "cookie": token,
                "prod_id": product_id,
                "flag": True,
            },
        )
        return item_id

    def view_cart(self, token: str) -> CartResponse | dict:
        response = self.requester.post(
            Endpoint.VIEW_CART,
            payload={"cookie": token, "flag": True},
        )
        body = response.body
        if isinstance(body, dict) and "errorMessage" in body:
            return body
        return CartResponse(**body)

    def delete_item(self, item_id: str) -> str:
        response = self.requester.post(
            Endpoint.DELETE_ITEM,
            payload={"id": item_id},
        )
        return response.body
