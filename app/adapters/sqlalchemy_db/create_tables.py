import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.adapters.sqlalchemy_db.models import Base


def create_tables() -> None:
    try:
        load_dotenv()
        db_uri = os.getenv('DATABASE_URI')
        if not db_uri:
            raise ValueError("DB_URI env variable is not set")
        engine = create_engine(db_uri, echo=True)
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except SQLAlchemyError as e:
        print(f"An error occurred while creating tables: {e}")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")


if __name__ == "__main__":
    create_tables()
