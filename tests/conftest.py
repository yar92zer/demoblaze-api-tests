import pytest

from api.custom_requester import CustomRequester
from api.services.catalog_service import CatalogService
from api.services.auth_service import AuthService
from utils.data_generator import unique_username, DEFAULT_PASSWORD
from api.services.cart_service import CartService


@pytest.fixture(scope="session")
def requester():
    return CustomRequester()


@pytest.fixture(scope="session")
def catalog(requester):
    return CatalogService(requester)


@pytest.fixture(scope="session")
def auth(requester):
    return AuthService(requester)


@pytest.fixture
def authenticated_user(auth):
    username = unique_username()
    auth.signup(username, DEFAULT_PASSWORD)
    token = auth.login(username, DEFAULT_PASSWORD)
    return {"username": username, "token": token}


@pytest.fixture(scope="session")
def cart(requester):
    return CartService(requester)


@pytest.fixture
def cart_with_product(cart, authenticated_user):
    item_id = cart.add_to_cart(authenticated_user["token"], product_id=1)
    yield {"item_id": item_id, "token": authenticated_user["token"]}
    cart.delete_item(item_id)
