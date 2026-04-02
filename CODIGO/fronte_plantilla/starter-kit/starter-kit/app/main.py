from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.routes.user import router
from app.db.session import engine
from app.db.base import Base

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


app.include_router(router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to MesaPass API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}

