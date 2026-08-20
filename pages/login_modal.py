from pages.base_page import BasePage


class LoginModal(BasePage):
    MODAL = "#logInModal"
    USERNAME_INPUT = "#loginusername"
    PASSWORD_INPUT = "#loginpassword"
    SUBMIT_BUTTON = "#logInModal button.btn-primary"
    CLOSE_BUTTON = "#logInModal button.btn-secondary"

    def wait_open(self) -> None:
        # Дождаться, пока модалка полностью раскроется.
        self.page.locator(f"{self.MODAL}.show").wait_for(
            state="visible", timeout=self.timeout
        )

    def login(self, username: str, password: str) -> None:
        # Заполнить форму и отправить.
        self.wait_open()
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)

    def login_expecting_alert(self, username: str, password: str) -> str:
        # Алерт прилетает из AJAX-коллбэка logIn(), поэтому хелпер, а не expect_event.
        self.wait_open()
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        return self.click_expecting_alert(self.SUBMIT_BUTTON)
