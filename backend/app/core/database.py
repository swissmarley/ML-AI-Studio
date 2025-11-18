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
    """Initialize database tables and create default test account"""
    try:
        from app.models import user, project, dataset, model  # noqa
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
        
        # Create default test account if it doesn't exist
        db = SessionLocal()
        try:
            from app.models.user import User
            from app.core.security import get_password_hash
            
            default_user = db.query(User).filter(User.username == "testuser").first()
            if not default_user:
                default_user = User(
                    email="test@example.com",
                    username="testuser",
                    hashed_password=get_password_hash("testpass123"),
                    full_name="Test User",
                    is_active=True,
                    is_superuser=False
                )
                db.add(default_user)
                db.commit()
                print("Default test account created: username='testuser', password='testpass123'")
            else:
                print("Default test account already exists")
        except Exception as e:
            print(f"Error creating default test account: {e}")
            db.rollback()
        finally:
            db.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't raise - allow app to start even if DB init fails
        # Tables will be created on first request if needed

