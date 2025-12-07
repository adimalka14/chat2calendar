from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.modules.auth.google_oauth_service import GoogleOAuthService

class GoogleAccessTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_prefixes=("/calendar",)):
        super().__init__(app)
        self.oauth = GoogleOAuthService()
        self.protected_prefixes = protected_prefixes

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        if any(path.startswith(p) for p in self.protected_prefixes):
            rt: Optional[str] = request.cookies.get("google_refresh_token")
            if not rt:
                return JSONResponse({"detail": "Missing refresh cookie"}, status_code=401)

            tokens = await self.oauth.refresh_access_token(rt)
            if not tokens or "access_token" not in tokens:
                return JSONResponse({"detail": "Failed to refresh Google access token"}, status_code=401)

            request.state.google_access_token = tokens["access_token"]

        return await call_next(request)
