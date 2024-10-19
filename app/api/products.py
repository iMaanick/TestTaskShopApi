from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from app.application.models.product import Product, ProductCreate, ProductUpdate
from app.application.products import new_product, get_product, update_product_db, delete_product_from_db, get_products
from app.application.protocols.database import DatabaseGateway, UoW

products_router = APIRouter()


@products_router.post("/", response_model=Product)
def create_product(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        product_data: ProductCreate,
) -> Product:
    """
    Creates a new product.
    """
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
    """
    Retrieves a list of products with optional filters.
    """
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
    return [Product.model_validate(product) for product in products]


@products_router.get("/{product_id}", response_model=Product)
def read_product(
        database: Annotated[DatabaseGateway, Depends()],
        product_id: int,
) -> Product:
    """
    Retrieves a product by its ID.
    """
    product = get_product(database, product_id)
    return product


@products_router.put("/{product_id}", response_model=Product)
def update_product(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        product_id: int,
        product_data: ProductUpdate

) -> Product:
    """
    Updates a product by its ID.
    """
    product = update_product_db(database, uow, product_id, product_data)
    return Product.model_validate(product)


@products_router.delete("/{product_id}", response_model=Product)
def delete_product(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        product_id: int,
) -> Product:
    """
    Deletes a product by its ID.
    """
    product = delete_product_from_db(database, uow, product_id)
    return product
