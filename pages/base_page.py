"""Базовый Page Object: общие действия поверх Playwright."""
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
