"""
Authentication routes for login/logout.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from backend.api.auth import create_access_token, verify_password
from backend.config import ADMIN_USERNAME, ADMIN_PASSWORD, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.api.auth import verify_token

router = APIRouter(prefix="/api", tags=["auth"])
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str

class UserResponse(BaseModel):
    username: str
    authenticated: bool

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Login endpoint - returns JWT token."""
    # Simple authentication against config (can be extended to use database)
    if login_data.username != ADMIN_USERNAME or login_data.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login_data.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": login_data.username
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(username: str = Depends(verify_token)):
    """Get current authenticated user info."""
    return {
        "username": username,
        "authenticated": True
    }

@router.post("/logout")
async def logout():
    """Logout endpoint (client should discard token)."""
    return {"message": "Logged out successfully"}

