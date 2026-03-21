from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_users


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users", response_model=List[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)
