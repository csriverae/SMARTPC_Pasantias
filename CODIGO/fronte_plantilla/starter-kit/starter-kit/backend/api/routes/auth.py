from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.crud.user import create_user, get_user_by_email, get_user
from backend.schemas.user import UserCreate, UserResponse
from backend.models.user import User
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.core.security import verify_password, create_access_token, create_refresh_token, decode_token


auth_router = APIRouter()
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    current_user = get_user(db, user_id)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return current_user


def require_role(role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role no autorizado")
        return current_user
    return role_checker


@auth_router.post("/register", response_model=None)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        return api_error("El email ya existe", status=400, error_data="duplicate email")
    try:
        new_user = create_user(db, user)
        return api_success("Usuario registrado", data={"id": str(new_user.id), "email": new_user.email, "name": new_user.name, "role": new_user.role}, status=201)
    except SQLAlchemyError as exc:
        return api_error("Error al consultar la lista negra de cédulas", status=500, error_data=str(exc))


@auth_router.post("/login")
def login(request: Request, form_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        return api_error("El email o la contraseña no coinciden con nuestros registros", status=404)
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return api_success("Login exitoso", data={"access_token": access_token, "refresh_token": refresh_token, "user": {"id": str(user.id), "name": user.name, "email": user.email, "role": user.role}})


@auth_router.post("/refresh")
def refresh(token: str):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        new_token = create_access_token({"sub": user_id})
        return api_success("Token renovado", data={"access_token": new_token})
    except Exception as exc:
        return api_error("Token inválido o expirado", status=401, error_data=str(exc))


@auth_router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return api_success("Usuario actual", data={"id": str(current_user.id), "email": current_user.email, "name": current_user.name, "role": current_user.role})
