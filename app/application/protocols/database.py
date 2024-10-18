from abc import ABC, abstractmethod
from typing import List

from app.adapters.sqlalchemy_db.models import Category as CategoryDB
from app.application.models.category import CategoryCreate, Category, CategoryUpdate
from app.application.models.product import Product


class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class DatabaseGateway(ABC):

    @abstractmethod
    def add_category(self, category: Category) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self, skip: int, limit: int) -> List[CategoryDB]:
        raise NotImplementedError

    @abstractmethod
    def get_category(self, category_id: int) -> CategoryDB:
        raise NotImplementedError

    @abstractmethod
    def delete_category(self, category: CategoryDB) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_category(self, category_data: CategoryUpdate, category: CategoryDB) -> CategoryDB:
        raise NotImplementedError

    @abstractmethod
    def add_product(self, product: Product) -> None:
        raise NotImplementedError