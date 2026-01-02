"""
Database configuration and session management.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import DATABASE_URL, BASE_DIR

# Prepare SQLite connection args and ensure directory exists
connect_args = {}
if 'sqlite' in DATABASE_URL:
    connect_args["check_same_thread"] = False
    # Ensure SQLite database directory exists
    if DATABASE_URL.startswith('sqlite:///'):
        db_path = DATABASE_URL.replace('sqlite:///', '')
        # Handle absolute paths
        if os.path.isabs(db_path):
            db_dir = os.path.dirname(db_path)
        else:
            # Relative path - use BASE_DIR
            db_path = str(BASE_DIR / db_path)
            db_dir = os.path.dirname(db_path)
        
        # Create directory if it doesn't exist
        if db_dir:
            try:
                os.makedirs(db_dir, exist_ok=True)
            except (OSError, PermissionError) as e:
                # If we can't create directory, try using /tmp as fallback
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Could not create database directory {db_dir}: {e}")
                # Use /tmp as fallback
                db_path = '/tmp/memos.db'
                DATABASE_URL = f'sqlite:///{db_path}'

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session (dependency for FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database by creating all tables."""
    from backend.api.models import Base
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error creating database tables: {e}")
        raise
