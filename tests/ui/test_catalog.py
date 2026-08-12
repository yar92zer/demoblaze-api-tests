import allure
import pytest

pytestmark = [pytest.mark.ui, allure.feature("Каталог UI")]


@pytest.mark.smoke
@allure.title("Витрина открывается в показывает товары")
def test_catalog_shows_products(home_page):
    home_page.open()
    assert home_page.get_products_count() == 9


@pytest.mark.regression
@allure.title("Фильтр по категории показывает только её товары")
def test_category_filters_products(home_page):
    home_page.open()
    home_page.open_category("Phones")
    assert home_page.get_products_count() == 7
