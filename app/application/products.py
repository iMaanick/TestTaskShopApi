from typing import List, Optional

from fastapi import HTTPException

from app.adapters.sqlalchemy_db.models import ProductDB
from app.application.models.product import ProductCreate, ProductUpdate
from app.application.protocols.database import UoW, ProductDatabaseGateway


def new_product(
        database: ProductDatabaseGateway,
        uow: UoW,
        product_data: ProductCreate,
) -> ProductDB:
    product = database.add_product(product_data)
    uow.commit()
    return product


def get_product(
        database: ProductDatabaseGateway,
        product_id: int,
) -> ProductDB:
    product = database.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def get_products(
        database: ProductDatabaseGateway,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_in_stock: Optional[int] = None,
        max_in_stock: Optional[int] = None,
        search_term: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
) -> List[ProductDB]:
    product = database.get_products(
        category_id,
        min_price,
        max_price,
        min_in_stock,
        max_in_stock,
        search_term,
        skip,
        limit,
    )
    return product


def update_product_db(
        database: ProductDatabaseGateway,
        uow: UoW,
        product_id: int,
        product_data: ProductUpdate
) -> ProductDB:
    product = database.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product = database.update_product(product_data, product)
    uow.commit()
    return product


def delete_product_from_db(
        database: ProductDatabaseGateway,
        uow: UoW,
        product_id: int,
) -> ProductDB:
    product = database.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    database.delete_product(product)
    uow.commit()
    return product
