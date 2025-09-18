"""
Authentication service for handling auth business logic.
"""

from typing import Tuple, Dict, Any, Optional
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings
from app.modules.auth.google_oauth_service import GoogleOAuthService

class AuthService:
    """Service for handling authentication business logic."""
    
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
    
    def create_access_token(self, data: Dict[str, str]) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Data to encode in token
            
        Returns:
            str: JWT access token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, str]]:
        """
        Verify JWT token and return payload.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Optional[Dict[str, str]]: Token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.JWTError:
            return None
    
    def create_user_session(self, user_data: Dict[str, str]) -> Dict[str, str]:
        """
        Create user session with access token.
        
        Args:
            user_data: User data to include in session
            
        Returns:
            Dict[str, str]: Session data with access token
        """
        access_token = self.create_access_token(user_data)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_data.get("sub"),
            "email": user_data.get("email")
        }

    async def login_with_google(self, code: str, google: GoogleOAuthService) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        tokens = await google.exchange_code_for_tokens(code)
        if not tokens or "access_token" not in tokens:
            raise ValueError("Token exchange failed")
        userinfo = await google.get_user_info(tokens["access_token"])
        if not userinfo or "sub" not in userinfo or "email" not in userinfo:
            raise ValueError("Userinfo fetch failed")
        return tokens, userinfo

    async def refresh_with_google(self, refresh_token: str, google: GoogleOAuthService) -> Tuple[
        Dict[str, Any], Dict[str, Any]]:
        tokens = await google.refresh_access_token(refresh_token)
        if not tokens or "access_token" not in tokens:
            raise ValueError("Google refresh failed")
        userinfo = await google.get_user_info(tokens["access_token"])
        if not userinfo or "sub" not in userinfo or "email" not in userinfo:
            raise ValueError("Userinfo fetch failed")
        return tokens, userinfo