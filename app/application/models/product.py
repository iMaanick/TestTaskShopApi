from dataclasses import field

from pydantic import BaseModel


class Product(BaseModel):
    id: int = field(init=False)
    name: str
    price: float
    in_stock: int

class ProductCreate(BaseModel):
    name: str
    price: float
    in_stock: int