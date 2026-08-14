"""Модалка оформления заказа и окно подтверждения покупки."""
from pages.base_page import BasePage


class OrderModal(BasePage):
    """Форма Place order на cart.html.

    Подтверждение после покупки рисует не браузерный `alert`, а
    SweetAlert (`node_modules/bootstrap-sweetalert`) — это обычный DOM,
    и читается он локаторами, а не обработчиком диалога.

    Валидация формы минимальна: `purchaseOrder()` проверяет только
    непустые Name и Credit card, остальные поля не смотрит. При пустых
    полях показывается нативный `alert`, а не подпись в `#errors`.
    """

    # Локаторы скоупим модалкой: id="errors" на cart.html продублирован —
    # он есть и здесь, и в модалке регистрации.
    MODAL = "#orderModal"
    TOTAL_LABEL = "#orderModal #totalm"
    NAME_INPUT = "#orderModal #name"
    COUNTRY_INPUT = "#orderModal #country"
    CITY_INPUT = "#orderModal #city"
    CARD_INPUT = "#orderModal #card"
    MONTH_INPUT = "#orderModal #month"
    YEAR_INPUT = "#orderModal #year"
    ERRORS_LABEL = "#orderModal #errors"

    # У кнопок своих id нет, различаем по классу внутри футера модалки.
    PURCHASE_BUTTON = "#orderModal button.btn-primary"
    CLOSE_BUTTON = "#orderModal button.btn-secondary"

    # Окно подтверждения SweetAlert — общее для страницы, не внутри модалки.
    CONFIRMATION = ".sweet-alert"
    CONFIRMATION_TITLE = ".sweet-alert h2"
    CONFIRMATION_TEXT = ".sweet-alert p"
    CONFIRMATION_OK_BUTTON = ".sweet-alert button.confirm"

    def wait_opened(self) -> None:
        """Дождаться, пока форма заказа станет видимой."""
        self.wait_visible(self.NAME_INPUT)

    def get_total(self) -> str:
        """Подпись с суммой в шапке формы, вида `Total: 360`."""
        return self.get_text(self.TOTAL_LABEL).strip()

    def fill_order(self, order: dict[str, str]) -> None:
        """Заполнить форму заказа.

        Ключи словаря: name, country, city, card, month, year. Отсутствующие
        поля не трогаются — так можно проверять частично заполненную форму.
        """
        fields = {
            "name": self.NAME_INPUT,
            "country": self.COUNTRY_INPUT,
            "city": self.CITY_INPUT,
            "card": self.CARD_INPUT,
            "month": self.MONTH_INPUT,
            "year": self.YEAR_INPUT,
        }
        for key, locator in fields.items():
            if key in order:
                self.fill(locator, order[key])

    def purchase(self) -> None:
        """Нажать Purchase и дождаться окна подтверждения."""
        self.click(self.PURCHASE_BUTTON)
        self.wait_visible(self.CONFIRMATION)

    def purchase_expecting_alert(self) -> str:
        """Нажать Purchase, когда ожидается отказ, и вернуть текст алерта.

        При пустых Name или Credit card форма показывает нативный
        `alert`, а не окно подтверждения. Алерт здесь синхронный —
        см. `BasePage.click_expecting_alert`.
        """
        return self.click_expecting_alert(self.PURCHASE_BUTTON)

    def get_confirmation_title(self) -> str:
        """Заголовок окна подтверждения."""
        return self.get_text(self.CONFIRMATION_TITLE).strip()

    def get_confirmation_text(self) -> str:
        """Тело подтверждения: id заказа, сумма, карта, имя, дата."""
        return self.get_text(self.CONFIRMATION_TEXT).strip()

    def confirm(self) -> None:
        """Закрыть подтверждение кнопкой OK.

        В `purchaseOrder()` на подтверждение навешен переход на главную
        (`location.href = 'index.html'`), но фактически его не происходит:
        окно закрывается, а адрес остаётся прежним — `cart.html`. Поэтому
        ждём исчезновения окна, а не навигацию. Заодно игнорируется и
        `closeOnConfirm: false` — окно закрывается вопреки настройке.
        """
        self.click(self.CONFIRMATION_OK_BUTTON)
        self.page.locator(self.CONFIRMATION).wait_for(state="hidden", timeout=self.timeout)

    def close(self) -> None:
        """Закрыть форму заказа, не покупая."""
        self.click(self.CLOSE_BUTTON)
