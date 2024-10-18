from sqlalchemy import Integer, String, Column, MetaData, Table, Float, Boolean, ForeignKey, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import registry, relationship, declarative_base


metadata_obj = MetaData()
mapper_registry = registry()

Base = declarative_base()

product_category_association = Table(
    'product_category', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    categories = relationship(
        "Category",
        secondary=product_category_association,
        back_populates="products"
    )


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    products = relationship(
        "Product",
        secondary=product_category_association,
        back_populates="categories"
    )

