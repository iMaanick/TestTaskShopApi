from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.application.models.category import Category


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int
    categories: List[Category] = []
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int
    categories: List[int] = []


class ProductUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int
    categories: List[int] = []
