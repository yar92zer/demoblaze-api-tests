import pytest

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
def login_page(page):
    return LoginModal(page, FRONT_URL, UI_TIMEOUT)

@pytest.fixture
def signup_page(page):
    return SignupModal(page, FRONT_URL, UI_TIMEOUT)

@pytest.fixture
def  header_page(page):
    return Header(page, FRONT_URL, UI_TIMEOUT)