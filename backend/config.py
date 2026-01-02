"""
Configuration settings for the backend.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
# Render: For production, use Render's PostgreSQL or set DATABASE_URL
# For SQLite, use persistent storage path
if os.getenv('RENDER'):
    # On Render, use persistent storage or PostgreSQL
    # Default to SQLite in /tmp for ephemeral storage (not recommended for production)
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///tmp/memos.db')
else:
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/memos.db')

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

