from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from backend.api.routes.auth import auth_router
from backend.api.routes.user import user_router
from backend.api.routes.restaurants import restaurant_router
from backend.api.routes.companies import company_router
from backend.api.routes.employees import employee_router
from backend.api.routes.agreements import agreement_router
from backend.api.routes.invitation_codes import invitation_router
from backend.api.routes.meal_logs import meal_log_router
from backend.db.session import engine
from backend.db.base import Base
from backend.models import *  # noqa: F401
from backend.core.response import api_success, api_error

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(restaurant_router, prefix="/restaurants", tags=["restaurants"])
app.include_router(company_router, prefix="/companies", tags=["companies"])
app.include_router(employee_router, prefix="/employees", tags=["employees"])
app.include_router(agreement_router, prefix="/agreements", tags=["agreements"])
app.include_router(invitation_router, prefix="/invitation-codes", tags=["invitation_codes"])
app.include_router(meal_log_router, prefix="/meal-logs", tags=["meal_logs"])


@app.get("/")
async def root():
    return api_success("API MesaPass v2 OK", data={})


@app.get("/health")
async def health():
    return api_success("health ok", data={})


@app.on_event("startup")
async def create_tables():
    Base.metadata.create_all(bind=engine)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Error al consultar la lista negra de cédulas",
            "status": 500,
            "error": True,
            "data": {
                "data": [],
                "error": str(exc),
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Error interno en el servidor",
            "status": 500,
            "error": True,
            "data": {"data": [], "error": str(exc)},
        },
    )

