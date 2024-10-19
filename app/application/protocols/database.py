from abc import ABC, abstractmethod
from typing import List, Optional
from app.adapters.sqlalchemy_db.models import ProductDB

from app.adapters.sqlalchemy_db.models import CategoryDB
from app.application.models.category import CategoryCreate, Category, CategoryUpdate
from app.application.models.product import Product, ProductCreate, ProductUpdate


class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class DatabaseGateway(ABC):

    @abstractmethod
    def add_category(self, category_data: CategoryCreate) -> CategoryDB:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self, skip: int, limit: int) -> List[CategoryDB]:
        raise NotImplementedError

    @abstractmethod
    def get_category(self, category_id: int) -> Optional[CategoryDB]:
        raise NotImplementedError

    @abstractmethod
    def delete_category(self, category: CategoryDB) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_category(self, category_data: CategoryUpdate, category: CategoryDB) -> CategoryDB:
        raise NotImplementedError

    @abstractmethod
    def add_product(self, product_data: ProductCreate) -> ProductDB:
        raise NotImplementedError

    @abstractmethod
    def get_product(self, product_id: int) -> Optional[ProductDB]:
        raise NotImplementedError

    @abstractmethod
    def update_product(self, product_data: ProductUpdate, product: ProductDB) -> ProductDB:
        raise NotImplementedError

    @abstractmethod
    def delete_product(self, product: ProductDB) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_products(
            self,
            category_id: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            min_in_stock: Optional[int] = None,
            max_in_stock: Optional[int] = None,
            search_term: Optional[str] = None,
            skip: int = 0,
            limit: int = 10,
    ) -> List[ProductDB]:
        raise NotImplementedError
