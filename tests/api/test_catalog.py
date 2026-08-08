import allure
import pytest


@pytest.mark.smoke
@allure.title("Каталог возвращает 9 товаров на страницу")
def test_entries_returns_nine_products(catalog):
    entries = catalog.get_entries()
    assert len(entries.Items) == 9
