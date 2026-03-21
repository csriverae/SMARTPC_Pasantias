from fastapi import FastAPI
from app.api.routes.user import router
from app.db.session import engine
from app.db.base import Base

# Import models so metadata is populated before create_all
from app.models.user import User  # noqa: F401

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health():
    return {"status": "ok"}

