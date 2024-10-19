from typing import List, Optional
from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from app.adapters.sqlalchemy_db.models import ProductDB, CategoryDB
from app.application.models.category import CategoryCreate, CategoryUpdate
from app.application.models.product import ProductUpdate, ProductCreate
from app.application.protocols.database import UoW, ProductDatabaseGateway, CategoryDatabaseGateway
from app.main.web import init_routers


class MockProductDatabase(ProductDatabaseGateway):
    def add_product(self, product_data: ProductCreate) -> ProductDB:
        return ProductDB(
            id=1,
            name=product_data.name,
            price=product_data.price,
            in_stock=product_data.in_stock
        )

    def get_product(self, product_id: int) -> Optional[ProductDB]:
        if product_id == 1:
            return ProductDB(id=1, name="Product 1", price=50.0, in_stock=5)
        return None

    def update_product(self, product_data: ProductUpdate, product: ProductDB) -> ProductDB:
        product.name = product_data.name
        return product

    def delete_product(self, product: ProductDB) -> None:
        return None

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
        if min_price == 60:
            return [
                ProductDB(id=2, name="Product 2", price=70.0, in_stock=3)
            ]
        if min_price == 1000:
            return []
        return [
            ProductDB(id=1, name="Product 1", price=50.0, in_stock=5),
            ProductDB(id=2, name="Product 2", price=70.0, in_stock=3)
        ]


class MockCategoryDatabase(CategoryDatabaseGateway):
    def add_category(self, category: CategoryCreate) -> CategoryDB:
        return CategoryDB(id=1, name=category.name, description=category.description)

    def get_categories(self, skip: int, limit: int) -> List[CategoryDB]:
        if skip == 0 and limit == 10:
            return [CategoryDB(id=1, name="Category 1"), CategoryDB(id=2, name="Category 2")]
        if skip == 1 and limit == 1:
            return [CategoryDB(id=2, name="Category 2")]
        if skip == 10 and limit is None:
            return []
        return []

    def get_category(self, category_id: int) -> Optional[CategoryDB]:
        if category_id == 1:
            return CategoryDB(id=1, name="Category 1")
        return None

    def delete_category(self, category: CategoryDB) -> None:
        return None

    def update_category(self, category_data: CategoryUpdate, category: CategoryDB) -> CategoryDB:
        return CategoryDB(id=1, name="Category 1")

    def get_products_by_category(self, category_id: int) -> Optional[List[ProductDB]]:
        if category_id == 1:
            return [
                ProductDB(id=1, name="Product 1", price=100.0, in_stock=5),
                ProductDB(id=2, name="Product 2", price=150.0, in_stock=3)
            ]
        if category_id == 2:
            return [
                ProductDB(id=3, name="Product 3", price=200.0, in_stock=10)
            ]
        if category_id == 3:
            return []
        return None


@fixture
def mock_uow() -> Mock:
    uow = Mock()
    uow.commit = Mock()
    uow.flush = Mock()
    return uow


@fixture
def client(mock_uow: UoW) -> TestClient:
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[ProductDatabaseGateway] = MockProductDatabase
    app.dependency_overrides[CategoryDatabaseGateway] = MockCategoryDatabase
    app.dependency_overrides[UoW] = lambda: mock_uow
    return TestClient(app)
