import pytest

from pages.home_page import HomePage
from settings import FRONT_URL, TIMEOUT


@pytest.fixture
def home_page(page):
    return HomePage(page, FRONT_URL, TIMEOUT * 1000)