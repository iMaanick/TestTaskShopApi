from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.api.depends_stub import Stub
from app.application.categories import new_category, get_categories, delete_category_from_db, get_category, \
    update_category_db, get_products_by_category
from app.application.models.category import CategoryCreate, Category, CategoryUpdate
from app.application.models.product import Product
from app.application.protocols.database import UoW, CategoryDatabaseGateway

categories_router = APIRouter()


class AddCategoriesResult(BaseModel):
    category_id: int


@categories_router.post("/", response_model=AddCategoriesResult)
def create_category(
        database: Annotated[CategoryDatabaseGateway, Depends(Stub(CategoryDatabaseGateway))],
        uow: Annotated[UoW, Depends()],
        category_data: CategoryCreate,
) -> AddCategoriesResult:
    """
    Creates a new category.
    """
    category_id = new_category(database, uow, category_data)
    return AddCategoriesResult(
        category_id=category_id,
    )


@categories_router.get("/", response_model=List[Category])
def list_categories(
        database: Annotated[CategoryDatabaseGateway, Depends(Stub(CategoryDatabaseGateway))],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0)] = 10,
) -> List[Category]:
    """
    Retrieves a list of categories with pagination.
    """
    categories = get_categories(database, skip, limit)
    return [Category.model_validate(category) for category in categories]


@categories_router.get("/{category_id}", response_model=Category)
def get_category_by_id(
        database: Annotated[CategoryDatabaseGateway, Depends(Stub(CategoryDatabaseGateway))],
        category_id: int,
) -> Category:
    """
    Retrieves a category by its ID.
    """
    category = get_category(database, category_id)
    return category


@categories_router.delete("/{category_id}", response_model=Category)
def delete_category(
        database: Annotated[CategoryDatabaseGateway, Depends(Stub(CategoryDatabaseGateway))],
        uow: Annotated[UoW, Depends()],
        category_id: int,
) -> Category:
    """
    Deletes a category by its ID.
    """
    category = delete_category_from_db(database, uow, category_id)
    return category


@categories_router.put("/{category_id}", response_model=Category)
def update_category(
        database: Annotated[CategoryDatabaseGateway, Depends(Stub(CategoryDatabaseGateway))],
        uow: Annotated[UoW, Depends()],
        category_id: int,
        category_data: CategoryUpdate

) -> Category:
    """
    Updates a category by its ID.
    """
    category = update_category_db(database, uow, category_id, category_data)
    return category


@categories_router.get("/{category_id}/products", response_model=List[Product])
def list_products_by_category(
        database: Annotated[CategoryDatabaseGateway, Depends(Stub(CategoryDatabaseGateway))],
        category_id: int,
) -> List[Product]:
    """
    Get products by a category ID.
    """
    products = get_products_by_category(database, category_id)
    return products
