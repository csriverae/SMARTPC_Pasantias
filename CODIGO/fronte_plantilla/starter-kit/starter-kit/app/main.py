"""
FastAPI application entry point with global middleware and exception handlers
"""
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.api.routes.user import router
from app.db.session import engine
from app.db.base import Base
from app.api.utils.response import (
    internal_error_response,
    not_found_response,
    unauthorized_response,
    forbidden_response,
    error_response,
    success_response,
)
from app.core.exceptions import (
    SaaSException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    ResourceNotFoundError,
    EmailAlreadyExists,
    InvalidCredentials,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models so metadata is populated before create_all
from app.models import User, Restaurant, Company, InvitationCode, Agreement, Employee, MealLog  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting MesaPass API...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    yield
    # Shutdown
    logger.info("Shutting down MesaPass API...")


# Create FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title="MesaPass SaaS API",
    description="Multi-tenant SaaS API for MesaPass",
    version="2.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/auth", tags=["Authentication"])


# Global Exception Handlers

@app.exception_handler(SaaSException)
async def saas_exception_handler(request: Request, exc: SaaSException):
    """Handle custom SaaS exceptions"""
    logger.warning(f"SaaS Exception: {exc.message} (Error Code: {exc.error_code})")
    body = error_response(
        message=exc.message,
        status_code=exc.status_code,
        error_code=exc.error_code,
        details=getattr(exc, 'details', None)
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(AuthenticationError)
async def authentication_error_handler(request: Request, exc: AuthenticationError):
    """Handle authentication errors"""
    logger.warning(f"Authentication Error: {exc.message}")
    body = unauthorized_response(
        message=exc.message,
        detail=getattr(exc, 'details', None),
        error_code=exc.error_code
    )
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=body)


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(request: Request, exc: AuthorizationError):
    """Handle authorization errors"""
    logger.warning(f"Authorization Error: {exc.message}")
    body = forbidden_response(
        message=exc.message,
        detail=getattr(exc, 'details', None)
    )
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=body)


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation Error: {exc.message}")
    body = error_response(
        message=exc.message,
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code="VALIDATION_ERROR",
        details=getattr(exc, 'details', None)
    )
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)


@app.exception_handler(ResourceNotFoundError)
async def not_found_error_handler(request: Request, exc: ResourceNotFoundError):
    """Handle not found errors"""
    logger.warning(f"Resource Not Found: {exc.message}")
    body = not_found_response(
        message=exc.message,
        detail=getattr(exc, 'details', None)
    )
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=body)


@app.exception_handler(EmailAlreadyExists)
async def email_exists_error_handler(request: Request, exc: EmailAlreadyExists):
    """Handle email already exists errors"""
    logger.warning(f"Email Already Exists: {exc.message}")
    body = error_response(
        message=exc.message,
        status_code=status.HTTP_409_CONFLICT,
        error_code=exc.error_code,
        details=getattr(exc, 'details', None)
    )
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=body)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTPException"""
    if exc.status_code == 404:
        body = not_found_response(detail=str(exc.detail) if exc.detail else "Not found")
        return JSONResponse(status_code=404, content=body)
    
    body = error_response(
        message=str(exc.detail) if exc.detail else "Error",
        status_code=exc.status_code,
        details=str(exc.detail) if exc.detail else None
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Internal Server Error: {str(exc)}", exc_info=True)
    body = internal_error_response(technical=str(exc))
    return JSONResponse(status_code=500, content=body)


# Health Check Endpoints

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return success_response(
        message="Welcome to MesaPass API v2.0",
        data={"docs": "/docs", "version": "2.0.0"}
    )


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return success_response(
        message="API is healthy",
        data={"status": "ok"}
    )

