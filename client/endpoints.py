from enum import StrEnum


class Endpoint(StrEnum):
    ENTRIES = "/entries"
    BYCAT = "/bycat"
    VIEW = "/view"
    SIGNUP = "/signup"
    LOGIN = "/login"
    ADD_TO_CART = "/addtocart"
    VIEW_CART = "/viewcart"
    DELETE_ITEM = "/deleteitem"
