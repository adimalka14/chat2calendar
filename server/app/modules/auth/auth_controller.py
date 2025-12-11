"""
Authentication controller for handling auth-related HTTP requests.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from typing import Optional
from app.config import settings
from app.dependencies import get_current_user
from app.modules.auth.models.auth_requests import (
    GoogleLoginRequest,
    GoogleLoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserInfoResponse,
    GetGoogleLoginUrlResponse
)
from app.modules.auth.google_oauth_service import GoogleOAuthService
from app.modules.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()
google_auth_service = GoogleOAuthService()


@router.post("/google", response_model=GoogleLoginResponse)
async def google_login(request: GoogleLoginRequest, response: Response):
    """
    Handle Google OAuth login.
    
    Args:
        request: Google login request with authorization code
        
    Returns:
        GoogleLoginResponse: JWT token and user info
    """
    try:
        tokens, userinfo = await auth_service.login_with_google(request.code, google_auth_service)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    rt = tokens.get("refresh_token")
    if rt:
        response.set_cookie(
            key="google_refresh_token",
            value=rt,
            httponly=True,
            samesite="none",
            secure=True,
            path="/",
            max_age=60*60*24*30,
        )

    uid = userinfo.get("sub") or userinfo.get("id")
    name = userinfo.get("name") or userinfo.get("given_name")
    picture = userinfo.get("picture")

    session = auth_service.create_user_session({
        "sub": uid,
        "email": userinfo["email"],
        "name": name,
        "picture": picture,
    })

    return GoogleLoginResponse(
        access_token=session["access_token"],
        token_type=session["token_type"],
        user_id=uid,
        email=userinfo["email"],
        expires_in=settings.access_token_expire_minutes * 60,
        name=name,  # ← חדש
        picture=picture,  # ← חדש
    )
@router.get("/google/login-url", response_model=GetGoogleLoginUrlResponse)
def get_login_url():
    url = google_auth_service.get_authorization_url()
    return GetGoogleLoginUrlResponse(login_url=url)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    google_refresh_token: Optional[str] = Cookie(None),
):
    """
    Refresh access token.

    Args:
        google_refresh_token

    Returns:
        RefreshTokenResponse: New access token
    """
    if not google_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh cookie")

    tokens, userinfo = await auth_service.refresh_with_google(google_refresh_token, google_auth_service)

    uid = userinfo.get("sub") or userinfo.get("id")
    name = userinfo.get("name") or userinfo.get("given_name")
    picture = userinfo.get("picture")

    jwt_token = auth_service.create_access_token({
        "sub": uid,
        "email": userinfo["email"],
        "name": name,
        "picture": picture,
    })

    return RefreshTokenResponse(
        access_token=jwt_token,
        token_type="bearer",
        user_id=uid,
        email=userinfo["email"],
        expires_in=settings.access_token_expire_minutes * 60,
        name=name,
        picture=picture,
    )
@router.post("/logout")
async def logout( response: Response, current_user: dict = Depends(get_current_user)):
    """
    Logout current user.
    
    Args:
        response: Response
        current_user: Current authenticated user
        
    Returns:
        dict: Logout confirmation
    """
    response.delete_cookie("google_refresh_token", path="/")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserInfoResponse: Current user information
    """
    return UserInfoResponse(
        user_id=current_user["user_id"],
        email=current_user["email"],
        name=current_user.get("name"),
        picture=current_user.get("picture"),
    )
