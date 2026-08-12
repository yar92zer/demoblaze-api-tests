"""Главная страница: витрина товаров, категории, пагинация."""
from collections.abc import Callable

from playwright.sync_api import Response

from pages.base_page import BasePage


class HomePage(BasePage):
    """Витрина с карточками товаров.

    Сетка рисуется скриптом `js/index.js` — в статическом HTML контейнер
    `#tbodyid` пустой. Переключение категории и страницы идёт через AJAX:
    скрипт делает `$('#tbodyid').empty()` и заполняет контейнер заново.
    Значит, сразу после клика старые карточки ещё в DOM, и проверка
    «карточки видны» прошла бы на старом содержимом.

    Поэтому ждём ответ бэкенда и сверяем отрисованное с тем, что в этом
    ответе пришло: он же и говорит, что должно оказаться на экране.
    """

    url_path = "index.html"

    # Эндпоинты, которые дёргает фронт при работе с витриной.
    BYCAT_ENDPOINT = "/bycat"
    PAGINATION_ENDPOINT = "/pagination"

    # --- категории (левое меню) ---
    # У всех трёх ссылок один и тот же id="itemc" — он не уникален, по нему
    # конкретную категорию не выбрать. Отбираем по видимому тексту.
    CATEGORY_LINKS = "a#itemc"
    CATEGORY_BY_NAME = "a#itemc:text-is('{name}')"

    # --- сетка товаров ---
    # Товар по названию строковым локатором не берём: название приходит из
    # каталога, и апостроф в нём сломает разбор селектора. См. open_product.
    PRODUCT_GRID = "#tbodyid"
    PRODUCT_CARDS = "#tbodyid .card"
    PRODUCT_TITLES = "#tbodyid a.hrefch"
    PRODUCT_PRICES = "#tbodyid .card-block h5"

    # --- пагинация ---
    NEXT_BUTTON = "#next2"
    PREVIOUS_BUTTON = "#prev2"

    # --- хедер ---
    # У ссылки Home своего id нет, берём по href внутри списка навигации:
    # снаружи тот же href висит на логотипе (a#nava).
    HOME_LINK = ".navbar-nav a[href='index.html']"
    CART_LINK = "#cartur"
    LOGIN_LINK = "#login2"
    SIGNUP_LINK = "#signin2"

    def open(self, path: str | None = None) -> None:
        """Открыть витрину и дождаться, пока скрипт нарисует карточки.

        `page.goto` возвращает управление по событию load, а товары
        приезжают отдельным запросом уже после него — без ожидания
        сетка будет пустой.
        """
        super().open(path)
        self.wait_for_products()

    def wait_for_products(self) -> None:
        """Дождаться первой карточки в сетке.

        `BasePage.wait_visible` тут не подходит: он ждёт локатор целиком,
        а для Playwright девять карточек в strict mode — ошибка, а не
        успех. Поэтому берём `.first`.
        """
        self.page.locator(self.PRODUCT_TITLES).first.wait_for(
            state="visible", timeout=self.timeout
        )

    def open_category(self, name: str) -> None:
        """Отфильтровать витрину по категории.

        `name` — подпись ссылки как она видна на странице: Phones,
        Laptops или Monitors.
        """
        with self.page.expect_response(self._response_from(self.BYCAT_ENDPOINT)) as caught:
            self.click(self.CATEGORY_BY_NAME.format(name=name))
        self._wait_until_rendered(caught.value)

    def get_product_titles(self) -> list[str]:
        """Названия товаров на текущей странице витрины."""
        return [text.strip() for text in self.page.locator(self.PRODUCT_TITLES).all_inner_texts()]

    def get_product_prices(self) -> list[str]:
        """Цены товаров на текущей странице, как они показаны: `$360`."""
        return [text.strip() for text in self.page.locator(self.PRODUCT_PRICES).all_inner_texts()]

    def get_products_count(self) -> int:
        """Сколько карточек показано сейчас."""
        return self.page.locator(self.PRODUCT_CARDS).count()

    def open_product(self, title: str) -> None:
        """Открыть карточку товара по названию.

        Берём нативный локатор, а не строку: название приходит из данных
        каталога, и апостроф в нём сломал бы разбор CSS-селектора.
        `get_by_role` экранирует текст сам.

        Кликаем именно по ссылке заголовка — у картинки карточки доступное
        имя пустое (alt=""), да и ведёт она на `prod.html` только в первой
        выдаче: после фильтра и пагинации скрипт ставит ей `href="#"`.
        """
        grid = self.page.locator(self.PRODUCT_GRID)
        grid.get_by_role("link", name=title, exact=True).click()

    def go_to_next_page(self) -> None:
        """Перейти на следующую страницу витрины."""
        with self.page.expect_response(self._response_from(self.PAGINATION_ENDPOINT)) as caught:
            self.click(self.NEXT_BUTTON)
        self._wait_until_rendered(caught.value)

    def go_to_previous_page(self) -> None:
        """Вернуться на предыдущую страницу витрины.

        Осторожно: стенд отдаёт по Previous набор со сдвигом на одну
        позицию — см. дефект в README. Метод воспроизводит поведение
        стенда как есть.
        """
        with self.page.expect_response(self._response_from(self.PAGINATION_ENDPOINT)) as caught:
            self.click(self.PREVIOUS_BUTTON)
        self._wait_until_rendered(caught.value)

    @staticmethod
    def _response_from(endpoint: str) -> Callable[[Response], bool]:
        """Предикат для `expect_response`: POST на нужный эндпоинт.

        Метод проверяем, чтобы не поймать предварительный OPTIONS-запрос
        CORS, который уходит на тот же адрес.
        """
        def predicate(response: Response) -> bool:
            return response.request.method == "POST" and response.url.endswith(endpoint)

        return predicate

    def _wait_until_rendered(self, response: Response) -> None:
        """Дождаться, пока в сетке окажется именно то, что пришло в ответе.

        Источник правды — тело ответа: какие товары бэкенд вернул, такие
        и должны быть отрисованы, в том же порядке. Сравнение с ответом,
        а не с прошлым состоянием, снимает две проблемы разом: не нужно
        трогать DOM приложения служебными метками, и повторный клик по той
        же категории не виснет — состав просто совпадает сразу.
        """
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
