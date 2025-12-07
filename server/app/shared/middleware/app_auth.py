from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.modules.auth.auth_service import AuthService

class AppAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_prefixes=("/calendar",)):
        super().__init__(app)
        self.protected_prefixes = protected_prefixes
        self.auth = AuthService()

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        if any(path.startswith(p) for p in self.protected_prefixes):
            auth_header: Optional[str] = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse({"detail": "Missing Authorization header"}, status_code=401)

            token = auth_header.split(" ", 1)[1].strip()
            payload = self.auth.verify_token(token)
            if not payload:
                return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)

            request.state.user = {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name"),
                "picture": payload.get("picture"),
            }

        return await call_next(request)
