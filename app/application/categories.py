from typing import List

from fastapi import HTTPException

from app.adapters.sqlalchemy_db.models import Category
from app.application.models.category import CategoryCreate, CategoryUpdate
from app.application.protocols.database import DatabaseGateway, UoW


def new_category(
        database: DatabaseGateway,
        uow: UoW,
        category_data: CategoryCreate,
) -> int:
    category = Category(name=category_data.name, description=category_data.description)
    database.add_category(category)
    uow.commit()
    return category.id


def get_categories(
        database: DatabaseGateway,
        skip: int,
        limit: int
) -> List[Category]:
    categories = database.get_categories(skip, limit)
    return categories


def delete_category_from_db(
        database: DatabaseGateway,
        uow: UoW,
        category_id: int,
) -> Category:
    category = database.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    database.delete_category(category)
    uow.commit()
    return category


def get_category(
        database: DatabaseGateway,
        category_id: int,
) -> Category:
    category = database.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category_db(
        database: DatabaseGateway,
        uow: UoW,
        category_id: int,
        category_data: CategoryUpdate
) -> Category:
    category = database.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = category_data.name
    category.description = category_data.description
    uow.commit()
    return category
