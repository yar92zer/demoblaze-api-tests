import allure
import pytest


@pytest.mark.smoke
@allure.title("Каталог возвращает 9 товаров на страницу")
def test_entries_returns_nine_products(catalog):
    entries = catalog.get_entries()
    assert len(entries.Items) == 9


@pytest.mark.regression
def test_by_category_returns_only_that_category(catalog):
    entries = catalog.get_by_category("phone")
    assert all(item.cat == "phone" for item in entries.Items)


@pytest.mark.smoke
def test_get_product_by_id(catalog):
    product = catalog.get_product("1")
    assert product.id == 1
