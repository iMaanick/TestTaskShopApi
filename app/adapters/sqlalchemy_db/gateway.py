from typing import List, Optional

from sqlalchemy.orm import Session
from app.adapters.sqlalchemy_db.models import Category as CategoryDB

from app.application.models.category import Category, CategoryUpdate
from app.application.models.product import Product
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_category(self, category: Category) -> int:
        self.session.add(category)
        return category.id

    def get_categories(self, skip: int, limit: int) -> List[CategoryDB]:
        categories = self.session.query(CategoryDB).offset(skip).limit(limit).all()
        return categories

    def get_category(self, category_id: int) -> Optional[CategoryDB]:
        category = self.session.get(CategoryDB, category_id)
        return category

    def delete_category(self, category: CategoryDB) -> None:
        self.session.delete(category)
        return

    def update_category(self, category_data: CategoryUpdate, category: CategoryDB) -> CategoryDB:
        category.name = category_data.name
        category.description = category_data.description
        return category

    def add_product(self, product: Product) -> None:
        self.session.add(product)
