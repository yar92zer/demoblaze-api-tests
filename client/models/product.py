from pydantic import BaseModel


class Product(BaseModel):
    id: int
    cat: str
    title: str
    price: float
    img: str
    desc: str

class PageKey(BaseModel):
    id: str

class EntriesResponse(BaseModel):
    Items: list[Product]
    LastEvaluatedKey: PageKey | None = None
