from enum import Enum


class Endpoint(str, Enum):
    ENTRIES = "/entries"
    BYCAT = "/bycat"
    VIEW = "/view"
    SIGNUP = "/signup"
    LOGIN = "/login"
    ADD_TO_CART = "/addtocart"
    VIEW_CART = "/viewcart"
    DELETE_ITEM = "/deleteitem"
