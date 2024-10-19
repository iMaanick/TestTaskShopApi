from typing import List, Optional

from sqlalchemy.orm import Session
from app.adapters.sqlalchemy_db.models import CategoryDB
from app.adapters.sqlalchemy_db.models import ProductDB
from app.application.models.category import Category, CategoryUpdate, CategoryCreate
from app.application.models.product import Product, ProductCreate, ProductUpdate
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_category(self, category_data: CategoryCreate) -> CategoryDB:
        category = CategoryDB(name=category_data.name, description=category_data.description)
        self.session.add(category)
        return category

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

    def add_product(self, product_data: ProductCreate) -> ProductDB:
        product = ProductDB(name=product_data.name,
                            description=product_data.description,
                            price=product_data.price,
                            in_stock=product_data.in_stock
                            )
        categories = self.session.query(CategoryDB).filter(CategoryDB.id.in_(product_data.categories)).all()
        product.categories = categories
        self.session.add(product)
        return product

    def get_product(self, product_id: int) -> Optional[ProductDB]:
        product = self.session.get(ProductDB, product_id)
        return product

    def update_product(self, product_data: ProductUpdate, product: ProductDB) -> ProductDB:
        product.name = product_data.name
        product.description = product_data.description
        product.in_stock = product_data.in_stock
        categories = self.session.query(CategoryDB).filter(CategoryDB.id.in_(product_data.categories)).all()
        product.categories = categories
        return product

    def delete_product(self, product: ProductDB) -> None:
        self.session.delete(product)
        return

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
        query = self.session.query(ProductDB)

        if category_id:
            query = query.join(ProductDB.categories).filter(CategoryDB.id == category_id)

        if min_price is not None:
            query = query.filter(ProductDB.price >= min_price)
        if max_price is not None:
            query = query.filter(ProductDB.price <= max_price)

        if min_in_stock is not None:
            query = query.filter(ProductDB.in_stock >= min_in_stock)
        if max_in_stock is not None:
            query = query.filter(ProductDB.in_stock <= max_in_stock)

        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                ProductDB.name.ilike(search_pattern) | ProductDB.description.ilike(search_pattern)
            )

        products = query.offset(skip).limit(limit).all()
        return products
