from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.crud.user import get_users, get_user, update_user, delete_user
from backend.schemas.user import UserUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.api.routes.auth import get_current_user, require_role
from backend.models.user import User

user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get("/", response_model=None)
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    data = [{"id": str(u.id), "name": u.name, "email": u.email, "role": u.role} for u in users]
    return api_success("Usuarios obtenidos", data={"users": data})


@user_router.get("/{user_id}", response_model=None)
def read_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user(db, user_id)
    if not user:
        return api_error("User not found", status=404)
    return api_success("Usuario encontrado", data={"user": {"id": str(user.id), "name": user.name, "email": user.email, "role": user.role}})


@user_router.put("/{user_id}", response_model=None)
def modify_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    user = update_user(db, user_id, payload)
    if not user:
        return api_error("User not found", status=404)
    return api_success("Usuario actualizado", data={"user": {"id": str(user.id), "name": user.name, "email": user.email, "role": user.role}})


@user_router.delete("/{user_id}", response_model=None)
def remove_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not delete_user(db, user_id):
        return api_error("User not found", status=404)
    return api_success("Usuario eliminado", data={})

