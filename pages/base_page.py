import time
from urllib.parse import urljoin

from playwright.sync_api import Page


class BasePage:
    url_path: str = ""

    def __init__(self, page: Page, base_url: str, timeout: int) -> None:
        self.page = page
        self.base_url = base_url
        self.timeout = timeout
        self.page.set_default_timeout(timeout)

    def open(self, path: str | None = None) -> None:
        self.page.goto(urljoin(self.base_url, path or self.url_path))

    def click(self, locator: str) -> None:
        self.page.locator(locator).click()

    def fill(self, locator: str, value: str) -> None:
        self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()

    def wait_visible(self, locator: str, timeout: int | None = None) -> None:
        self.page.locator(locator).wait_for(state="visible", timeout=timeout or self.timeout)

    def click_expecting_alert(self, locator: str, accept: bool = True) -> str:
        # Обработчик вешается ДО клика намеренно: алерты из onclick
        # (purchaseOrder, send) блокируют страницу синхронно, click() не
        # вернёт управление, и expect_event вокруг клика уйдёт в таймаут.
        captured: list[str] = []

        def handler(dialog) -> None:
            captured.append(dialog.message)
            if accept:
                dialog.accept()
            else:
                dialog.dismiss()

        self.page.once("dialog", handler)
        self.click(locator)

        # Асинхронный алерт приходит уже после возврата из click.
        deadline = time.monotonic() + self.timeout / 1000
        while not captured and time.monotonic() < deadline:
            self.page.wait_for_timeout(50)

        if not captured:
            raise AssertionError(f"Диалог не появился после клика по {locator!r}")
        return captured[0]
