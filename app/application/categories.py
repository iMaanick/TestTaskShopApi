from typing import List

from fastapi import HTTPException

from app.adapters.sqlalchemy_db.models import CategoryDB, ProductDB
from app.application.models.category import CategoryCreate, CategoryUpdate
from app.application.protocols.database import DatabaseGateway, UoW


def new_category(
        database: DatabaseGateway,
        uow: UoW,
        category_data: CategoryCreate,
) -> int:
    category = database.add_category(category_data)
    uow.commit()
    return category.id


def get_categories(
        database: DatabaseGateway,
        skip: int,
        limit: int
) -> List[CategoryDB]:
    categories = database.get_categories(skip, limit)
    return categories


def get_category(
        database: DatabaseGateway,
        category_id: int,
) -> CategoryDB:
    category = database.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def delete_category_from_db(
        database: DatabaseGateway,
        uow: UoW,
        category_id: int,
) -> CategoryDB:
    category = database.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    database.delete_category(category)
    uow.commit()
    return category


def update_category_db(
        database: DatabaseGateway,
        uow: UoW,
        category_id: int,
        category_data: CategoryUpdate
) -> CategoryDB:
    category = database.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category = database.update_category(category_data, category)
    uow.commit()
    return category


def get_products_by_category(
        database: DatabaseGateway,
        category_id: int,

) -> List[ProductDB]:
    products = database.get_products_by_category(category_id)
    if products is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return products
