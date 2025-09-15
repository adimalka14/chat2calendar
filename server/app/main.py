from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    print('dev')
    return {"status": "health"}


# """
# Main FastAPI application for Chat2Calendar server.
# """
#
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.config import settings
# from app.modules.auth.controllers.auth_controller import router as auth_router
# from app.modules.calendar.controllers.calendar_controller import router as calendar_router
# from app.modules.ai.controllers.ai_controller import router as ai_router
# from app.shared.middleware.error_handler import (
#     http_exception_handler,
#     validation_exception_handler,
#     chat2calendar_exception_handler,
#     general_exception_handler
# )
# from app.shared.exceptions.base_exceptions import Chat2CalendarException
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException
#
# # Create FastAPI application
# app = FastAPI(
#     title=settings.app_name,
#     version=settings.app_version,
#     description="AI-powered Google Calendar integration server",
#     docs_url="/docs" if settings.debug else None,
#     redoc_url="/redoc" if settings.debug else None,
# )
#
# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.allowed_origins,
#     allow_credentials=True,
#     allow_methods=settings.allowed_methods,
#     allow_headers=settings.allowed_headers,
# )
#
# # Add exception handlers
# app.add_exception_handler(StarletteHTTPException, http_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(Chat2CalendarException, chat2calendar_exception_handler)
# app.add_exception_handler(Exception, general_exception_handler)
#
# # Include routers
# app.include_router(auth_router)
# app.include_router(calendar_router)
# app.include_router(ai_router)
#
#
# @app.get("/")
# async def root():
#     """Root endpoint with basic information."""
#     return {
#         "message": "Welcome to Chat2Calendar Server",
#         "version": settings.app_version,
#         "status": "running"
#     }
#
#
# @app.get("/health")
# async def health_check():
#     """Health check endpoint."""
#     return {"status": "healthy", "version": settings.app_version}
#
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "app.main:app",
#         host=settings.host,
#         port=settings.port,
#         reload=settings.debug
#     )
