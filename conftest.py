import pytest
import allure

from utils.encoders import encode_password
from pages.header import Header
from pages.home_page import HomePage
from pages.login_modal import LoginModal
from pages.product_page import ProductPage
from pages.signup_modal import SignupModal
from settings import FRONT_URL, TIMEOUT
from pages.cart_page import CartPage
from client.custom_requester import CustomRequester
from client.services.auth_service import AuthService
from client.services.cart_service import CartService
from client.services.catalog_service import CatalogService
from utils.data_generator import DEFAULT_PASSWORD, unique_username
from pages.contact_modal import ContactModal
from pages.order_modal import OrderModal

UI_TIMEOUT = TIMEOUT * 1000


@pytest.fixture
def home_page(page):
    return HomePage(page, FRONT_URL, UI_TIMEOUT)


@pytest.fixture
def product_page(page):
    return ProductPage(page, FRONT_URL, UI_TIMEOUT)


@pytest.fixture
def login_modal(page):
    return LoginModal(page, FRONT_URL, UI_TIMEOUT)


@pytest.fixture
def signup_modal(page):
    return SignupModal(page, FRONT_URL, UI_TIMEOUT)


@pytest.fixture
def header(page):
    return Header(page, FRONT_URL, UI_TIMEOUT)


@pytest.fixture
def registered_user(auth):
    username = unique_username()
    auth.signup(username, encode_password(DEFAULT_PASSWORD))
    return {"username": username, "password": DEFAULT_PASSWORD}


@pytest.fixture
def logged_in_user(page, home_page, header, login_modal, registered_user):
    home_page.open()
    header.open_login_modal()
    with page.expect_navigation():
        login_modal.login(registered_user["username"], registered_user["password"])
    page.locator(header.USERNAME_LABEL).wait_for(state="visible", timeout=UI_TIMEOUT)
    return registered_user


@pytest.fixture
def cart_page(page):
    return CartPage(page, FRONT_URL, UI_TIMEOUT)


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


@pytest.fixture
def order_modal(page):
    return OrderModal(page, FRONT_URL, UI_TIMEOUT)


@pytest.fixture
def contact_modal(page):
    return ContactModal(page, FRONT_URL, UI_TIMEOUT)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    page = item.funcargs.get("page")
    if page is None:
        return

    allure.attach(
        page.screenshot(full_page=True),
        name="Скриншот при падении",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        page.url,
        name="URL",
        attachment_type=allure.attachment_type.TEXT,
    )
