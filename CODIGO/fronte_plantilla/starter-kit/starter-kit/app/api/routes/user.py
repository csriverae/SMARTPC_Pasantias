from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import traceback
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, PasswordChangeRequest
from app.schemas.response import SuccessResponse, ErrorResponse
from app.crud.user import create_user, get_users, authenticate_user, get_user_by_email, delete_user, update_user_password
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    require_roles,
    verify_token,
)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user exists using get_user_by_email
        db_user = get_user_by_email(db, user.email)
        if db_user:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "El email ya está registrado",
                    "status": 400,
                    "error": True,
                    "data": {"data": []}
                }
            )
        
        registered_user = create_user(db, user)
        return JSONResponse(
            status_code=201,
            content={
                "message": "Usuario registrado exitosamente",
                "status": 201,
                "error": False,
                "data": {
                    "data": [{
                        "id": registered_user.id,
                        "email": registered_user.email,
                        "full_name": registered_user.full_name,
                        "role": registered_user.role.value
                    }]
                }
            }
        )
    except ValueError as ve:
        # Handle validation errors (e.g., password too long)
        print(f"Validation error: {ve}")
        return JSONResponse(
            status_code=400,
            content={
                "message": "Error de validación",
                "status": 400,
                "error": True,
                "data": {
                    "data": [],
                    "error": str(ve)
                }
            }
        )
    except Exception as e:
        error_msg = str(e)
        if "72" in error_msg or "bytes" in error_msg:
            error_msg = "La contraseña es demasiado larga. Máximo 72 bytes UTF-8 permitidos"
        if "UndefinedColumn" in error_msg or "no existe la columna" in error_msg:
            error_msg = "Error en la estructura de la base de datos. Ejecute rebuild_db.py para reconstruir las tablas."
        
        print(f"Registration error: {e}")
        print(traceback.format_exc())
        
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al registrar el usuario",
                "status": 500,
                "error": True,
                "data": {
                    "data": [],
                    "error": error_msg
                }
            }
        )


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = authenticate_user(db, user.email, user.password)
        if not db_user:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "El email o la contraseña no coinciden con nuestros registros",
                    "status": 401,
                    "error": True,
                    "data": {"data": []}
                }
            )

        token_data = {"sub": db_user.email, "role": db_user.role.value}
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Inicio de sesión exitoso",
                "status": 200,
                "error": False,
                "data": {
                    "data": [{
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_type": "bearer"
                    }]
                }
            }
        )
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Error de validación",
                "status": 400,
                "error": True,
                "data": {
                    "data": [],
                    "error": str(ve)
                }
            }
        )
    except Exception as e:
        print(f"Login error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al iniciar sesión",
                "status": 500,
                "error": True,
                "data": {
                    "data": [],
                    "error": str(e)
                }
            }
        )


@router.post("/refresh")
def refresh_token(refresh: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = verify_token(refresh.refresh_token)
        if payload is None or payload.get("sub") is None:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Token de refresco inválido",
                    "status": 401,
                    "error": True,
                    "data": {"data": []}
                }
            )

        user = get_user_by_email(db, payload.get("sub"))
        if user is None:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Usuario no encontrado",
                    "status": 401,
                    "error": True,
                    "data": {"data": []}
                }
            )

        token_data = {"sub": user.email, "role": user.role.value}
        new_access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token(data=token_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Token refrescado exitosamente",
                "status": 200,
                "error": False,
                "data": {
                    "data": [{
                        "access_token": new_access_token,
                        "refresh_token": new_refresh_token,
                        "token_type": "bearer"
                    }]
                }
            }
        )
    except Exception as e:
        print(f"Refresh token error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al refrescar el token",
                "status": 500,
                "error": True,
                "data": {
                    "data": [],
                    "error": str(e)
                }
            }
        )


@router.get("/me")
def get_current_user_endpoint(current_user=Depends(get_current_user)):
    try:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Usuario obtenido exitosamente",
                "status": 200,
                "error": False,
                "data": {
                    "data": [{
                        "id": current_user.id,
                        "email": current_user.email,
                        "full_name": current_user.full_name,
                        "role": current_user.role.value
                    }]
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener usuario actual",
                "status": 500,
                "error": True,
                "data": {"data": [], "error": str(e)}
            }
        )


@router.get("/users")
def get_users_endpoint(current_user=Depends(require_roles("admin")), db: Session = Depends(get_db)):
    try:
        users = get_users(db)
        users_data = [{
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value
        } for user in users]
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Usuarios obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": users_data}
            }
        )
    except Exception as e:
        print(f"Get users error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener usuarios",
                "status": 500,
                "error": True,
                "data": {"data": [], "error": str(e)}
            }
        )


@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, current_user=Depends(require_roles("admin")), db: Session = Depends(get_db)):
    try:
        if not delete_user(db, user_id):
            return JSONResponse(
                status_code=404,
                content={
                    "message": "Usuario no encontrado",
                    "status": 404,
                    "error": True,
                    "data": {"data": []}
                }
            )
        return JSONResponse(
            status_code=200,
            content={
                "message": "Usuario eliminado exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": []}
            }
        )
    except Exception as e:
        print(f"Delete user error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al eliminar usuario",
                "status": 500,
                "error": True,
                "data": {"data": [], "error": str(e)}
            }
        )


@router.post("/change-password")
def change_password(password_change: PasswordChangeRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Validate passwords match
        if password_change.new_password != password_change.confirm_password:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Las nuevas contraseñas no coinciden",
                    "status": 400,
                    "error": True,
                    "data": {"data": []}
                }
            )
        
        # Validate new password is not empty
        if not password_change.new_password or len(password_change.new_password) < 6:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "La nueva contraseña debe tener al menos 6 caracteres",
                    "status": 400,
                    "error": True,
                    "data": {"data": []}
                }
            )
        
        # Get fresh user from database using the new db session
        from app.core.security import verify_password
        user = get_user_by_email(db, current_user.email)
        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "message": "Usuario no encontrado",
                    "status": 404,
                    "error": True,
                    "data": {"data": []}
                }
            )
        
        # Verify current password
        if not verify_password(password_change.current_password, user.password):
            return JSONResponse(
                status_code=401,
                content={
                    "message": "La contraseña actual es incorrecta",
                    "status": 401,
                    "error": True,
                    "data": {"data": []}
                }
            )
        
        # Update password
        update_user_password(db, user, password_change.new_password)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Contraseña cambiada exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": []}
            }
        )
    except Exception as e:
        print(f"Change password error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al cambiar contraseña",
                "status": 500,
                "error": True,
                "data": {"data": [], "error": str(e)}
            }
        )
