"""
Database configuration and session management - SQLite Version
Type annotations fixed for Pylance
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging
from .models import Base

logger = logging.getLogger(__name__)

# Database configuration from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./shopify_insights.db"
)

# Create engine for SQLite
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

async def init_db() -> None:
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

class DatabaseManager:
    """Database manager for handling operations"""
    
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def create(self, model_instance):
        """Create a new record"""
        try:
            self.db.add(model_instance)
            self.db.commit()
            self.db.refresh(model_instance)
            return model_instance
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating record: {e}")
            raise
    
    def get_by_id(self, model_class, record_id):
        """Get record by ID"""
        return self.db.query(model_class).filter(model_class.id == record_id).first()
    
    def get_by_field(self, model_class, field_name: str, field_value):
        """Get record by specific field"""
        return self.db.query(model_class).filter(
            getattr(model_class, field_name) == field_value
        ).first()
    
    def update(self, model_instance, **kwargs):
        """Update a record"""
        try:
            for key, value in kwargs.items():
                setattr(model_instance, key, value)
            self.db.commit()
            self.db.refresh(model_instance)
            return model_instance
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating record: {e}")
            raise
    
    def bulk_create(self, model_instances):
        """Create multiple records"""
        try:
            self.db.add_all(model_instances)
            self.db.commit()
            return model_instances
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error bulk creating records: {e}")
            raise