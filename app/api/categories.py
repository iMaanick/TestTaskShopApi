from typing import Annotated, List

from pydantic import BaseModel

from app.application.categories import new_category, get_categories, delete_category_from_db, get_category, \
    update_category_db
from app.application.models.category import CategoryCreate, Category, CategoryUpdate
from app.application.protocols.database import DatabaseGateway, UoW
from fastapi import APIRouter, Depends, Query

categories_router = APIRouter()


class AddCategoriesResult(BaseModel):
    category_id: int


@categories_router.post("/", response_model=AddCategoriesResult)
def create_category(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        category_data: CategoryCreate,
) -> AddCategoriesResult:
    category_id = new_category(database, uow, category_data)
    return AddCategoriesResult(
        category_id=category_id,
    )


@categories_router.get("/", response_model=List[Category])
def read_categories(
        database: Annotated[DatabaseGateway, Depends()],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0)] = 10,
) -> List[Category]:
    categories = get_categories(database, skip, limit)
    return categories


@categories_router.delete("/{category_id}", response_model=Category)
def delete_category(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        category_id: int,
):
    category = delete_category_from_db(database, uow, category_id)
    return category


@categories_router.get("/{category_id}", response_model=Category)
def read_category(
        database: Annotated[DatabaseGateway, Depends()],
        category_id: int,
):
    category = get_category(database, category_id)
    return category


@categories_router.put("/{category_id}", response_model=Category)
def update_category(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        category_id: int,
        category_data: CategoryUpdate

):
    category = update_category_db(database, uow, category_id, category_data)
    return category
