from pages.base_page import BasePage


class ProductPage(BasePage):
    url_path = "prod.html"
    TITLE = "#tbodyid h2.name"
    PRICE = "#tbodyid h3.price-container"
    DESCRIPTION = "#more-information p"
    ADD_TO_CART_BUTTON = "#tbodyid a.btn-success"
    IMAGE = "#imgp img"

    def open_by_id(self, product_id: int) -> None:
        self.open(f"{self.url_path}?idp_={product_id}")
        self.wait_for_product()

    def wait_for_product(self):
        # Дождаться,пока скрипт нарисует карточку.
        self.wait_visible(self.TITLE)

    def get_title(self) -> str:
        self.wait_for_product()
        return self.get_text(self.TITLE).strip()

    def get_description(self) -> str:
        self.wait_for_product()
        return self.get_text(self.DESCRIPTION).strip()

    def add_to_cart(self) -> str:
        self.wait_for_product()
        return self.click_expecting_alert(self.ADD_TO_CART_BUTTON)

    def get_price(self) -> str:
        # Цена и налог лежат в одном h3: "$650 *includes tax".
        # Отрезаем хвост, чтобы сравнивать с ценой на витрине.
        self.wait_for_product()
        return self.get_text(self.PRICE).split("*")[0].strip()
