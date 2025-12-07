from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.modules.auth.auth_controller import router as auth_router
from app.modules.ai.ai_controller import router as ai_router
from app.shared.middleware.app_auth import AppAuthMiddleware
from app.shared.middleware.google_token import GoogleAccessTokenMiddleware

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

app.add_middleware(
    AppAuthMiddleware,
    protected_prefixes=("/ai",))
app.add_middleware(
    GoogleAccessTokenMiddleware,
    protected_prefixes=("/ai",))

app.include_router(auth_router)
app.include_router(ai_router)

@app.get("/health")
def health():
    return {"status": "ok"}