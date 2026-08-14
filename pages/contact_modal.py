"""Модалка обратной связи (Contact)."""
from pages.base_page import BasePage


class ContactModal(BasePage):
    """Форма New message, открывается ссылкой Contact в шапке.

    Форма ничего не отправляет на бэкенд: `send()` в `js/index.js`
    очищает поля, показывает нативный `alert` и перезагружает страницу.
    Проверять здесь можно только реакцию интерфейса.
    """

    MODAL = "#exampleModal"
    EMAIL_INPUT = "#recipient-email"
    NAME_INPUT = "#recipient-name"
    MESSAGE_INPUT = "#message-text"

    # У кнопки Send message своего id нет, различаем по классу в футере.
    SEND_BUTTON = "#exampleModal button.btn-primary"
    CLOSE_BUTTON = "#exampleModal button.btn-secondary"

    def wait_opened(self) -> None:
        """Дождаться, пока модалка станет видимой."""
        self.wait_visible(self.EMAIL_INPUT)

    def send_message(self, email: str, name: str, message: str) -> str:
        """Заполнить форму, отправить и вернуть текст алерта.

        Алерт ловим через `expect_event`: без явного ожидания Playwright
        закрывает диалог сам и текст прочитать уже негде.
        """
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.NAME_INPUT, name)
        self.fill(self.MESSAGE_INPUT, message)
        return self.click_expecting_alert(self.SEND_BUTTON)

    def close(self) -> None:
        """Закрыть модалку без отправки."""
        self.click(self.CLOSE_BUTTON)
