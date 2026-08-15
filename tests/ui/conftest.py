import pytest

from utils.data_generator import unique_username, DEFAULT_PASSWORD
from utils.encoders import encode_password
from pages.header import Header
from pages.home_page import HomePage
from pages.login_modal import LoginModal
from pages.product_page import ProductPage
from pages.signup_modal import SignupModal
from settings import FRONT_URL, TIMEOUT

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
