"""
Configuration settings for the backend.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
# Render: For production, use Render's PostgreSQL or set DATABASE_URL
# For SQLite, ensure directory exists and is writable
DATABASE_URL_ENV = os.getenv('DATABASE_URL', '')

if DATABASE_URL_ENV:
    # Use provided DATABASE_URL (PostgreSQL on Render, or custom)
    DATABASE_URL = DATABASE_URL_ENV
elif os.getenv('RENDER'):
    # On Render without DATABASE_URL, use /tmp (ephemeral - not recommended)
    # Note: Data will be lost on redeploy. Use PostgreSQL instead!
    import warnings
    warnings.warn("Using SQLite on Render - data will be lost on redeploy. Use PostgreSQL!")
    db_path = '/tmp/memos.db'
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    except (OSError, PermissionError):
        # If /tmp doesn't work, try current directory
        db_path = str(BASE_DIR / 'memos.db')
    DATABASE_URL = f'sqlite:///{db_path}'
else:
    # Local development: use project directory
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

