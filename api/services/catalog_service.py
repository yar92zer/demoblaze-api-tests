from api.services.base_service import BaseService
from config.endpoints import Endpoint
from api.models.product import EntriesResponse, Product


class CatalogService(BaseService):
    def get_entries(self) -> EntriesResponse:
        response = self.requester.get(Endpoint.ENTRIES)
        return EntriesResponse(**response.body)

    def get_by_category(self, category: str) -> EntriesResponse:
        response = self.requester.post(Endpoint.BYCAT, payload={"cat": category})
        return EntriesResponse(**response.body)

    def get_product(self, product_id: str) -> Product:
        response = self.requester.post(Endpoint.VIEW, payload={"id": product_id})
        return Product(**response.body)
