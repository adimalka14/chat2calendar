"""
FastAPI dependencies for the Chat2Calendar server.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from app.modules.auth.auth_service import AuthService


# Security scheme
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_service = AuthService()

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "name": payload.get("name"),
        "picture": payload.get("picture"),
    }

def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[dict]:
    """
    Get current authenticated user from JWT token (optional).
    Returns None if no valid token is provided.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        dict | None: User information from token or None
    """
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None
