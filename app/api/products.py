from typing import Annotated, List, Optional

from pydantic import BaseModel

from app.application.categories import new_category, get_categories, delete_category_from_db, get_category, \
    update_category_db
from app.application.models.category import CategoryCreate, Category, CategoryUpdate
from app.application.models.product import Product, ProductCreate, ProductUpdate
from app.application.products import new_product, get_product, update_product_db, delete_product_from_db, get_products
from app.application.protocols.database import DatabaseGateway, UoW
from fastapi import APIRouter, Depends, Query

products_router = APIRouter()


@products_router.post("/", response_model=Product)
def create_product(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        product_data: ProductCreate,
) -> Product:
    product = new_product(database, uow, product_data)
    return product


@products_router.get("/", response_model=List[Product])
def read_products(
        database: Annotated[DatabaseGateway, Depends()],
        category_id: Optional[int] = None,
        min_price: Annotated[Optional[float], Query(ge=0)] = None,
        max_price: Annotated[Optional[float], Query(ge=0)] = None,
        min_in_stock: Annotated[Optional[int], Query(ge=0)] = None,
        max_in_stock: Annotated[Optional[int], Query(ge=0)] = None,
        search_term: Optional[str] = None,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0)] = 10,
) -> List[Product]:
    products = get_products(
        database,
        category_id,
        min_price,
        max_price,
        min_in_stock,
        max_in_stock,
        search_term,
        skip,
        limit,
    )
    return products


@products_router.get("/{product_id}", response_model=Product)
def read_product(
        database: Annotated[DatabaseGateway, Depends()],
        product_id: int,
) -> Product:
    product = get_product(database, product_id)
    return product


@products_router.put("/{product_id}", response_model=Product)
def update_product(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        product_id: int,
        product_data: ProductUpdate

) -> Product:
    product = update_product_db(database, uow, product_id, product_data)
    return product


@products_router.delete("/{product_id}", response_model=Product)
def delete_category(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        product_id: int,
) -> Product:
    product = delete_product_from_db(database, uow, product_id)
    return product
