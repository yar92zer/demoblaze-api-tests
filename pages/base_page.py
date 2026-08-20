import time
from urllib.parse import urljoin

from playwright.sync_api import Page


class BasePage:
    """Родитель всех страниц и модалок.

    Держит объект страницы Playwright и таймаут ожиданий. Наследники
    объявляют свои локаторы классовыми атрибутами и пользуются
    обёртками отсюда, чтобы не дублировать ожидания в каждом методе.
    """

    # Путь относительно base_url. Переопределяется в наследниках.
    url_path: str = ""

    def __init__(self, page: Page, base_url: str, timeout: int) -> None:
        """Запомнить страницу, базовый адрес и таймаут ожиданий."""
        self.page = page
        self.base_url = base_url
        self.timeout = timeout
        self.page.set_default_timeout(timeout)

    def open(self, path: str | None = None) -> None:
        """Открыть страницу.

        Без аргумента открывает `url_path` наследника, с аргументом —
        переданный путь.
        """
        self.page.goto(urljoin(self.base_url, path or self.url_path))

    def click(self, locator: str) -> None:
        """Дождаться видимости элемента и кликнуть по нему."""
        self.page.locator(locator).click()

    def fill(self, locator: str, value: str) -> None:
        """Очистить поле и ввести значение."""
        self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        """Вернуть видимый текст элемента."""
        return self.page.locator(locator).inner_text()

    def wait_visible(self, locator: str, timeout: int | None = None) -> None:
        """Дождаться, пока элемент станет видимым.

        Без `timeout` используется значение из настроек.
        """
        self.page.locator(locator).wait_for(state="visible", timeout=timeout or self.timeout)

    def click_expecting_alert(self, locator: str, accept: bool = True) -> str:
        """Кликнуть и вернуть текст нативного диалога.

        Обработчик вешается ДО клика намеренно. Demoblaze показывает
        алерты двумя способами: часть — синхронно прямо в обработчике
        onclick (`purchaseOrder`, `send`), часть — из коллбэка AJAX
        (`addToCart`, `logIn`). В синхронном случае alert блокирует
        страницу, и `click()` не вернёт управление, пока диалог не снят,
        поэтому обёртка `expect_event` вокруг клика уходит в дедлок.
        Здесь же диалог снимается сразу, а текст остаётся сохранённым.

        Без обработчика Playwright закрывает диалог сам и текст теряется.
        """
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
