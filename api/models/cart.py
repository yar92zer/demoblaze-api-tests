from pydantic import BaseModel


class CartItem(BaseModel):
    id: str
    cookie: str
    prod_id: int


class CartResponse(BaseModel):
    Items: list[CartItem]
