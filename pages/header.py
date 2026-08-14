from pages.base_page import BasePage


class Header(BasePage):
    HOME_LINK = ".navbar-nav a[href.'index.html']"
    CART_LINK = "#cartur"
    LOGIN_LINK = "#login2"
    SIGNUP_LINK = "signin2"
    LOGOUT_LINK = "#logout2"
    USERNAME_LINK = "#nameofuser"
    CONTACT_LINK = "a[data-target='#exampleModal']"
    ABOUT_LINK = "a[data-target='#videoModal']"


def open_login_modal(self) -> None:
    # Открыть модалку входа.
    self.click(self.LOGIN_LINK)


def open_signup_modal(self) -> None:
    # Открыть модалку регистрации.
    self.click(self.SIGNUP_LINK)


def open_contact_modal(self) -> None:
    # Открыть модалку контактов.
    self.click(self.CONTACT_LINK)


def open_cart(self) -> None:
    # Перейти в карзину.
    self.click(self.CART_LINK)


def get_logged_user(self) -> str:
    # Имя вошедшего пользователя без приставки Welcome.
    self.wait_visible(self.USERNAME_LABEL)
    return self.get_text(self.USERNAME_LABEL).replace("Welcome ", "").strip()


def is_logged_in(self) -> bool:
    # Показывает ли шапка, что пользователь вошёл.
    return self.page.locator(self.LOGIN_LABEL).is_visible()


def logout(self) -> None:
    # Выйти. logOut() чистит кукку и уводит на index.html.
    self.click(self.LOGOUT_LINK)
