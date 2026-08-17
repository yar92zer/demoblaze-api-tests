from collections.abc import Callable

from playwright.sync_api import Response

from pages.base_page import BasePage


class CartPage(BasePage):
    url_path = "cart.html"

    VIEWCART_ENDPOINT = "/viewcart"

    # --- таблица позиций ---
    TABLE_BODY = "#tbodyid"
    ROWS = "#tbodyid tr"
    ROW_TITLES = "#tbodyid tr td:nth-child(2)"
    ROW_PRICES = "#tbodyid tr td:nth-child(3)"
    DELETE_LINKS = "#tbodyid tr td:nth-child(4) a"

    # --- итог и оформление ---
    # У #totalp свой id, у кнопки Place Order — нет, берём по data-target.
    TOTAL = "#totalp"
    PLACE_ORDER_BUTTON = "button[data-target='#orderModal']"

    def open(self, path: str | None = None) -> None:
        """Открыть корзину и дождаться, пока таблица будет отрисована."""
        with self.page.expect_response(self._response_from(self.VIEWCART_ENDPOINT)) as caught:
            super().open(path)
        self._wait_until_rendered(caught.value)

    def get_item_titles(self) -> list[str]:
        """Названия позиций в корзине. Порядок не гарантирован."""
        return [text.strip() for text in self.page.locator(self.ROW_TITLES).all_inner_texts()]

    def get_item_prices(self) -> list[int]:
        """Цены позиций числами, в том же порядке, что и названия."""
        return [int(text.strip()) for text in self.page.locator(self.ROW_PRICES).all_inner_texts()]

    def get_total(self) -> int:
        """Итоговая сумма, как её посчитал сайт.

        У пустой корзины `#totalp` пустой — возвращаем 0.
        """
        raw = self.get_text(self.TOTAL).strip()
        return int(raw) if raw else 0

    def get_items_count(self) -> int:
        """Сколько позиций сейчас в таблице."""
        return self.page.locator(self.ROWS).count()

    def is_empty(self) -> bool:
        """Пуста ли корзина."""
        return self.get_items_count() == 0

    def delete_item(self, title: str) -> None:
        """Удалить позицию по названию товара.

        После удаления `cart.js` делает `location.reload()`, поэтому ждём
        новый цикл отрисовки, а не просто исчезновение строки.
        """
        row = self.page.locator(self.ROWS).filter(has_text=title)
        with self.page.expect_response(self._response_from(self.VIEWCART_ENDPOINT)) as caught:
            row.locator("a").click()
        self._wait_until_rendered(caught.value)

    def place_order(self) -> None:
        """Открыть модалку оформления заказа."""
        self.click(self.PLACE_ORDER_BUTTON)

    @staticmethod
    def _response_from(endpoint: str) -> Callable[[Response], bool]:
        """Предикат для `expect_response`: POST на нужный эндпоинт."""
        def predicate(response: Response) -> bool:
            return response.request.method == "POST" and response.url.endswith(endpoint)

        return predicate

    def _wait_until_rendered(self, response: Response) -> None:
        """Дождаться, пока в таблице окажется столько строк, сколько позиций.

        Пустая корзина проходит проверку сразу — строк ноль, позиций ноль.
        """
        body = response.json()
        expected = len(body.get("Items", [])) if isinstance(body, dict) else 0
        self.page.wait_for_function(
            "expected => document.querySelectorAll('#tbodyid tr').length === expected",
            arg=expected,
            timeout=self.timeout,
        )
