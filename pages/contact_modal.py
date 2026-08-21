from pages.base_page import BasePage


class ContactModal(BasePage):
    MODAL = "#exampleModal"
    EMAIL_INPUT = "#recipient-email"
    NAME_INPUT = "#recipient-name"
    MESSAGE_INPUT = "#message-text"

    # У кнопки Send message своего id нет, различаем по классу в футере.
    SEND_BUTTON = "#exampleModal button.btn-primary"
    CLOSE_BUTTON = "#exampleModal button.btn-secondary"

    def wait_opened(self) -> None:
        self.wait_visible(self.EMAIL_INPUT)

    def send_message(self, email: str, name: str, message: str) -> str:
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.NAME_INPUT, name)
        self.fill(self.MESSAGE_INPUT, message)
        return self.click_expecting_alert(self.SEND_BUTTON)

    def close(self) -> None:
        self.click(self.CLOSE_BUTTON)
