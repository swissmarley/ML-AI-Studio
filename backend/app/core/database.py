"""Database configuration and initialization"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from app.core.config import settings

# PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB
mongo_client = MongoClient(settings.MONGODB_URL)
mongodb = mongo_client.mlai_studio


def get_db():
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables"""
    try:
        from app.models import user, project, dataset, model  # noqa
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't raise - allow app to start even if DB init fails
        # Tables will be created on first request if needed

