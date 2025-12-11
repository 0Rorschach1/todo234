import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()


def get_database_url() -> str:
    """Get the database URL from environment variables."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/todolist",
    )


def get_engine() -> Engine:
    """Create and return the SQLAlchemy engine."""
    database_url = get_database_url()
    return create_engine(database_url, echo=False)


# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_session() -> Generator[Session, None, None]:
    """Get a database session. Use as a context manager or generator."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
