import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

try:
    DB_HOST = os.getenv("DB_HOST") or "localhost"
    DB_PORT = int(os.getenv("DB_PORT") or 5432)
    DB_NAME = os.getenv("DB_NAME") or "healthcare_db"
    DB_USER = os.getenv("DB_USER") or "postgres"
    DB_PASS = os.getenv("DB_PASSWORD") or ""
except (TypeError, ValueError):
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "healthcare_db"
    DB_USER = "postgres"
    DB_PASS = ""

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()