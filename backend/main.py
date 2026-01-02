"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (
    API_VERSION,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    ENVIRONMENT
)
from backend.api.database import init_db
from backend.api.routes import memos, stats

# Create FastAPI app
app = FastAPI(
    title="Digital Diary API",
    description="Backend API for managing diary memos",
    version=API_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(memos.router)
app.include_router(stats.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Digital Diary API",
        "version": API_VERSION,
        "environment": ENVIRONMENT
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        init_db()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to initialize database: {e}")
        # Don't fail startup if database init fails (might be first run)
        # The database will be created on first use

if __name__ == "__main__":
    import uvicorn
    from backend.config import API_HOST, API_PORT, API_RELOAD
    
    # For local development
    uvicorn.run(
        "backend.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD
    )

# For Render deployment:
# Render will automatically detect FastAPI and use gunicorn with uvicorn workers
# The app object is directly importable as: backend.main:app
# Render will bind to the PORT environment variable automatically

