from collections.abc import Callable

from playwright.sync_api import Response

from pages.base_page import BasePage


class HomePage(BasePage):
    url_path = "index.html"
    BYCAT_ENDPOINT = "/bycat"
    PAGINATION_ENDPOINT = "/pagination"
    CATEGORY_LINKS = "a#itemc"
    # id="itemc" продублирован на всех трёх категориях, поэтому голый
    # #itemc даёт strict mode violation - различаем по тексту.
    CATEGORY_BY_NAME = "a#itemc:text-is('{name}')"
    PRODUCT_GRID = "#tbodyid"
    PRODUCT_CARDS = "#tbodyid .card"
    PRODUCT_TITLES = "#tbodyid a.hrefch"
    PRODUCT_PRICES = "#tbodyid .card-block h5"
    NEXT_BUTTON = "#next2"
    PREVIOUS_BUTTON = "#prev2"
    HOME_LINK = ".navbar-nav a[href='index.html']"
    CART_LINK = "#cartur"
    LOGIN_LINK = "#login2"
    SIGNUP_LINK = "#signin2"

    def open(self, path: str | None = None) -> None:
        super().open(path)
        self.wait_for_products()

    def wait_for_products(self) -> None:
        self.page.locator(self.PRODUCT_TITLES).first.wait_for(
            state="visible", timeout=self.timeout
        )

    def open_category(self, name: str) -> None:
        with self.page.expect_response(self._response_from(self.BYCAT_ENDPOINT)) as caught:
            self.click(self.CATEGORY_BY_NAME.format(name=name))
        self._wait_until_rendered(caught.value)

    def get_product_titles(self) -> list[str]:
        return [text.strip() for text in self.page.locator(self.PRODUCT_TITLES).all_inner_texts()]

    def get_product_prices(self) -> list[str]:
        return [text.strip() for text in self.page.locator(self.PRODUCT_PRICES).all_inner_texts()]

    def get_products_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARDS).count()

    def open_product(self, title: str) -> None:
        grid = self.page.locator(self.PRODUCT_GRID)
        grid.get_by_role("link", name=title, exact=True).click()

    def go_to_next_page(self) -> None:
        with self.page.expect_response(self._response_from(self.PAGINATION_ENDPOINT)) as caught:
            self.click(self.NEXT_BUTTON)
        self._wait_until_rendered(caught.value)

    def go_to_previous_page(self) -> None:
        with self.page.expect_response(self._response_from(self.PAGINATION_ENDPOINT)) as caught:
            self.click(self.PREVIOUS_BUTTON)
        self._wait_until_rendered(caught.value)

    @staticmethod
    def _response_from(endpoint: str) -> Callable[[Response], bool]:
        def predicate(response: Response) -> bool:
            return response.request.method == "POST" and response.url.endswith(endpoint)

        return predicate

    def _wait_until_rendered(self, response: Response) -> None:
        expected = [item["title"].strip() for item in response.json().get("Items", [])]
        self.page.wait_for_function(
            """expected => {
                const titles = [...document.querySelectorAll('#tbodyid a.hrefch')]
                    .map(link => link.textContent.trim());
                return titles.length === expected.length
                    && titles.every((title, index) => title === expected[index]);
            }""",
            arg=expected,
            timeout=self.timeout,
        )
