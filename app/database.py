import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = None
SessionLocal = None

def _init_db():
    global engine, SessionLocal
    if engine is not None:
        return
    try:
        engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Database engine created successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        engine = None
        SessionLocal = None

_init_db()


class Base(DeclarativeBase):
    pass


def get_db():
    if SessionLocal is None:
        _init_db()
    if SessionLocal is None:
        raise Exception("Database not available")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
