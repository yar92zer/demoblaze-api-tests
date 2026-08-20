from pages.base_page import BasePage


class SignupModal(BasePage):
    MODAL = "#signInModal"
    USERNAME_INPUT = "#sign-username"
    PASSWORD_INPUT = "#sign-password"
    ERROR_LABEL = "#signInModal #errors"
    SUBMIT_BUTTON = "#signInModal button.btn-primary"
    CLOSE_BUTTON = "#signInModal button.btn-secondary"

    def wait_open(self) -> None:
        # Дождаться раскрытия модалки.
        self.page.locator(f"{self.MODAL}.show").wait_for(
            state="visible", timeout=self.timeout
        )

    def register(self, username: str, password: str) -> str:
        # Зарегистрировать пользователя, вернуть текст алерта.
        self.wait_open()
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        return self.click_expecting_alert(self.SUBMIT_BUTTON)
