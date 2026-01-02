"""
Configuration settings for the backend.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
# Render: Use PostgreSQL (free tier) for persistent data storage
# For SQLite, ensure directory exists and is writable (local dev only)
DATABASE_URL_ENV = os.getenv('DATABASE_URL', '')

if DATABASE_URL_ENV:
    # Use provided DATABASE_URL (PostgreSQL on Render, or custom)
    # Render provides postgres:// but SQLAlchemy needs postgresql://
    # Use psycopg (v3) dialect for Python 3.13+ compatibility
    if DATABASE_URL_ENV.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL_ENV.replace('postgres://', 'postgresql+psycopg://', 1)
    elif DATABASE_URL_ENV.startswith('postgresql://') and not DATABASE_URL_ENV.startswith('postgresql+'):
        # Convert postgresql:// to postgresql+psycopg:// to use psycopg3
        DATABASE_URL = DATABASE_URL_ENV.replace('postgresql://', 'postgresql+psycopg://', 1)
    else:
        DATABASE_URL = DATABASE_URL_ENV
elif os.getenv('RENDER'):
    # On Render without DATABASE_URL - this should not happen!
    # PostgreSQL database should be created and linked in Render Dashboard
    import warnings
    import logging
    logger = logging.getLogger(__name__)
    logger.error("⚠️ DATABASE_URL not set on Render! Creating PostgreSQL database is required.")
    warnings.warn("⚠️ CRITICAL: DATABASE_URL not set on Render. Data will be lost!")
    warnings.warn("Create a PostgreSQL database in Render Dashboard and link it to your service.")
    # Fallback to SQLite (will lose data - NOT RECOMMENDED)
    db_path = '/tmp/memos.db'
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    except (OSError, PermissionError):
        db_path = str(BASE_DIR / 'memos.db')
    DATABASE_URL = f'sqlite:///{db_path}'
else:
    # Local development: use SQLite in project directory
    db_path = BASE_DIR / 'memos.db'
    DATABASE_URL = f'sqlite:///{db_path}'

# API configuration
# Render provides PORT environment variable, use it if available
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('PORT', os.getenv('API_PORT', 8001)))
API_RELOAD = os.getenv('API_RELOAD', 'false').lower() == 'true'  # Disable reload in production by default

# CORS configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
CORS_ALLOW_CREDENTIALS = os.getenv('CORS_ALLOW_CREDENTIALS', 'true').lower() == 'true'

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# API version
API_VERSION = "1.0.0"

# Authentication configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production-min-32-chars')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# Default admin credentials (should be changed via environment variables)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')  # Change this in production!

