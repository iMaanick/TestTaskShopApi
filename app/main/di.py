import os
from functools import partial
from logging import getLogger
from typing import Iterable, Generator

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.sqlalchemy_db.gateway import ProductSqlaGateway, CategorySqlaGateway
from app.api.depends_stub import Stub
from app.application.protocols.database import UoW, ProductDatabaseGateway, CategoryDatabaseGateway

logger = getLogger(__name__)


def new_product_gateway(session: Session = Depends(Stub(Session))) -> Generator[ProductSqlaGateway, None, None]:
    yield ProductSqlaGateway(session)


def new_category_gateway(session: Session = Depends(Stub(Session))) -> Generator[CategorySqlaGateway, None, None]:
    yield CategorySqlaGateway(session)


def new_uow(session: Session = Depends(Stub(Session))) -> Session:
    return session


def create_session_maker() -> sessionmaker[Session]:
    load_dotenv()
    db_uri = os.getenv('DATABASE_URI')
    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return sessionmaker(engine, autoflush=False, expire_on_commit=False)


def new_session(session_maker: sessionmaker[Session]) -> Iterable[Session]:
    with session_maker() as session:
        yield session


def init_dependencies(app: FastAPI) -> None:
    session_maker = create_session_maker()

    app.dependency_overrides[Session] = partial(new_session, session_maker)
    app.dependency_overrides[ProductDatabaseGateway] = new_product_gateway
    app.dependency_overrides[CategoryDatabaseGateway] = new_category_gateway
    app.dependency_overrides[UoW] = new_uow
