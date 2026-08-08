import pytest

from api.custom_requester import CustomRequester
from api.services.catalog_service import CatalogService

@pytest.fixture(scope="session")
def requester():
    return CustomRequester()

@pytest.fixture(scope="session")
def catalog(requester):
    return CatalogService(requester)