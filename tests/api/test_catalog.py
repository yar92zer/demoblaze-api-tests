import allure
import pytest

pytestmark = allure.feature("Каталог")


@pytest.mark.smoke
@allure.title("Каталог возвращает непустой список валидных товаров")
def test_entries_returns_products(catalog):
    entries = catalog.get_entries()
    assert entries.Items
    assert all(item.id and item.title and item.price > 0 for item in entries.Items)


@pytest.mark.regression
@allure.title("Размер страницы каталога 9 товаров")
def test_entries_page_size(catalog):
    entries = catalog.get_entries()
    assert len(entries.Items) == 9


@pytest.mark.regression
@allure.title("Фильтр по категории возвращает только товары этой категории")
def test_by_category_returns_only_that_category(catalog):
    entries = catalog.get_by_category("phone")
    assert all(item.cat == "phone" for item in entries.Items)


@pytest.mark.smoke
@allure.title("Товар доступен по идентификатору")
def test_get_product_by_id(catalog):
    product = catalog.get_product("1")
    assert product.id == 1
