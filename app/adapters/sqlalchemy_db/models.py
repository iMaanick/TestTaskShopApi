from typing import Optional, List

from sqlalchemy import Integer, String, Column, MetaData, Table, Float, ForeignKey
from sqlalchemy.orm import registry, relationship, declarative_base, Mapped, mapped_column

metadata_obj = MetaData()
mapper_registry = registry()

Base = declarative_base()

product_category_association = Table(
    'product_category',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class ProductDB(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[int] = mapped_column(Integer, default=0)
    categories: Mapped[list["CategoryDB"]] = relationship(
        "CategoryDB",
        secondary=product_category_association,
        back_populates="products"
    )


class CategoryDB(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    products: Mapped[List[ProductDB]] = relationship(
        "ProductDB",
        secondary=product_category_association,
        back_populates="categories",
    )
