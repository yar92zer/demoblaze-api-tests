import allure
import pytest

pytestmark = [pytest.mark.ui, allure.feature("Каталог UI")]


@pytest.mark.smoke
@allure.title("Витрина открывается в показывает и товары")
def test_catalog_shows_products(home_page):
    home_page.open()
    assert home_page.get_products_count() == 9


@pytest.mark.regression
@allure.title("Фильтр по категории показывает только её товары")
def test_category_filters_products(home_page):
    home_page.open()
    home_page.open_category("Phones")
    assert home_page.get_products_count() == 7


@pytest.mark.regression
@allure.title("Переход на следующую страницу меняет набор товаров")
def test_next_page_shows_other_products(home_page):
    home_page.open()
    first = home_page.get_product_titles()
    home_page.go_to_next_page()
    second = home_page.get_product_titles()
    assert set(first) & set(second) == set()


@pytest.mark.smoke
@allure.title("Клик по товару открывает его карточку")
def test_open_product_card(home_page, product_page):
    home_page.open()
    home_page.open_product("Nexus 6")
    assert product_page.get_title() == "Nexus 6"


@pytest.mark.regression
@allure.title("Цена в карточке совпадает с ценой на витрине")
def test_price_matches_catalog(home_page, product_page):
    home_page.open()
    catalog_price = home_page.get_product_prices()[0]
    title = home_page.get_product_titles()[0]
    home_page.open_product(title)
    assert product_page.get_price() == catalog_price
