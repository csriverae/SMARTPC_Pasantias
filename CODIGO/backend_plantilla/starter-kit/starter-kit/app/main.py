from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.routers.auth import router as auth_router
from app.api.routers.employees import router as employees_router
from app.api.routers.users import router as users_router
from app.api.routers.invitations import router as invitations_router
from app.api.routers.agreements import router as agreements_router
from app.api.routers.meal_logs import router as meal_logs_router
from app.api.routers.qr import router as qr_router
from app.api.routers.reports import router as reports_router
from app.api.routes.entities import router as entities_router
from app.db.session import engine
from app.db.base import Base

# Import models so metadata is populated before create_all
from app.models import User, Restaurant, Company, InvitationCode, Agreement, Employee, MealLog, Tenant, UserTenant  # noqa: F401


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


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle pydantic validation errors with custom format"""
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Error de validación en los datos enviados",
            "status": 422,
            "error": True,
            "data": {
                "data": [],
                "errors": errors
            }
        }
    )


# New SaaS Multi-Tenant Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(employees_router, prefix="/api", tags=["entities"])
app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(invitations_router, prefix="/api", tags=["invitations"])
app.include_router(agreements_router, prefix="/api", tags=["agreements"])
app.include_router(meal_logs_router, prefix="/api", tags=["meal-logs"])
app.include_router(qr_router, prefix="/api", tags=["qr"])
app.include_router(reports_router, prefix="/api", tags=["reports"])

# Legacy routers (kept for backward compatibility during migration)
app.include_router(entities_router, prefix="/api", tags=["entities"])


@app.get("/")
async def root():
    return {"message": "Welcome to MesaPass API - SaaS Multi-Tenant", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}

