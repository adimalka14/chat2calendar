"""
Google OAuth service for handling Google authentication.
"""
from urllib.parse import urlencode
from typing import Dict, Optional
import httpx
from app.config import settings


class GoogleOAuthService:
    """Service for handling Google OAuth authentication."""
    
    def __init__(self):
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.scopes = settings.google_calendar_scopes
    
    def get_authorization_url(self) -> str:
        """
        Get Google OAuth authorization URL.
        
        Returns:
            str: Authorization URL for Google OAuth
        """
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        scope_str = f"openid email profile {self.scopes}".strip()

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope_str,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }

        return f"{base_url}?{urlencode(params)}"

    async def exchange_code_for_tokens(self, code: str) -> Optional[Dict[str, str]]:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            code: Authorization code from Google
            
        Returns:
            Optional[Dict[str, str]]: Tokens if successful, None otherwise
        """
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, str]]:
        """
        Get user information from Google using access token.
        
        Args:
            access_token: Google access token
            
        Returns:
            Optional[Dict[str, str]]: User info if successful, None otherwise
        """
        user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.get(user_info_url, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Google refresh token
            
        Returns:
            Optional[Dict[str, str]]: New tokens if successful, None otherwise
        """
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None