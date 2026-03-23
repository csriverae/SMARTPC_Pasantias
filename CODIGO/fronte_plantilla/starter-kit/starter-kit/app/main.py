from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.include_router(router, prefix="/auth", tags=["auth"])


@app.get("/health")
async def health():
    return {"status": "ok"}

