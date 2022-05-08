import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/test_fast_api"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL") # docker compose

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

""" alembic init migrations """


Base.metadata.create_all(bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
