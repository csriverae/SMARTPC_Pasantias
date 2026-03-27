from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.routes.user import router
from app.db.session import engine
from app.db.base import Base
from app.api.utils.response import StandardResponse, internal_error_response, not_found_response

# Import models so metadata is populated before create_all
from app.models import User, Restaurant, Company, InvitationCode, Agreement, Employee, MealLog  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/auth", tags=["auth"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        body = not_found_response(detail=str(exc.detail) if exc.detail else "Not found")
        return JSONResponse(status_code=404, content=body)
    body = {
        "message": str(exc.detail) if exc.detail else "Error",
        "status": exc.status_code,
        "error": True,
        "data": {"error": str(exc.detail) if exc.detail else "Error"},
    }
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    body = internal_error_response(technical=str(exc))
    return JSONResponse(status_code=500, content=body)


@app.get("/")
async def root():
    return {
        "message": "Welcome to MesaPass API",
        "status": 200,
        "error": False,
        "data": {"docs": "/docs"},
    }


@app.get("/health")
async def health():
    return {
        "message": "API health check",
        "status": 200,
        "error": False,
        "data": {"status": "ok"},
    }

