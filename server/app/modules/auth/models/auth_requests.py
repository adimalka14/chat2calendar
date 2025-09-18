"""
Authentication request/response models.
"""

from pydantic import BaseModel
from typing import Optional


class GoogleLoginRequest(BaseModel):
    """Google OAuth login request."""
    
    code: str
    state: Optional[str] = None


class GoogleLoginResponse(BaseModel):
    """Google OAuth login response."""
    
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    expires_in: int
    name: Optional[str] = None
    picture: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Refresh token response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None


class UserInfoResponse(BaseModel):
    """User information response."""
    
    user_id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None


class LogoutResponse(BaseModel):
    """Logout response."""
    
    message: str = "Logged out successfully"


class GetGoogleLoginUrlResponse(BaseModel):
    """Get login url response."""
    login_url: str