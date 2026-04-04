"""Authentication Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.schemas.user import UserLogin
from app.services.auth_service import AuthService
from app.core.security import generate_unique_token, get_current_user


router = APIRouter()


class UserRegister(BaseModel):
    email: str
    password: str
    tenant_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", tags=["Authentication"])
def register(register_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register endpoint - creates tenant and owner user
    Headers required: None
    """
    try:
        user, tenant, user_tenant = AuthService.register_owner(
            db=db,
            email=register_data.email,
            password=register_data.password,
            tenant_name=register_data.tenant_name
        )

        tokens = AuthService.create_tokens(
            user_id=user.id,
            tenant_id=str(tenant.id),
            email=user.email,
            role=user_tenant.role
        )

        return JSONResponse(
            status_code=201,
            content={
                "message": "Registro exitoso",
                "status": 201,
                "error": False,
                "data": {
                    "data": {
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"],
                        "token_type": tokens["token_type"],
                        "tenant_id": str(tenant.id),
                        "user": {
                            "user_id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "tenant_role": user_tenant.role
                        }
                    }
                }
            }
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail,
                "status": e.status_code,
                "error": True,
                "data": {"data": None}
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error en registro: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.post("/login", tags=["Authentication"])
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login endpoint - returns access_token, tenant_id, and user info
    Headers required: None for login
    """
    try:
        user = AuthService.authenticate_user(db, credentials.email, credentials.password)
        tenants = AuthService.get_user_tenants(db, user.id)

        if not tenants:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario no tiene acceso a ningún tenant"
            )

        first_tenant = tenants[0]
        tokens = AuthService.create_tokens(
            user_id=user.id,
            tenant_id=first_tenant["tenant_id"],
            email=user.email,
            role=first_tenant["role"]
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "Login exitoso",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"],
                        "token_type": tokens["token_type"],
                        "tenant_id": first_tenant["tenant_id"],
                        "user": {
                            "user_id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "tenant_role": first_tenant["role"],
                            "tenants": tenants
                        }
                    }
                }
            }
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail,
                "status": e.status_code,
                "error": True,
                "data": {"data": None}
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error en login: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.post("/refresh-token", tags=["Authentication"])
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    try:
        from app.core.security import verify_token
        
        payload = verify_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )
        
        email = payload.get("sub")
        from app.crud.user import get_user_by_email
        user = get_user_by_email(db, email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )
        
        # Create new access token
        new_tokens = AuthService.create_tokens(
            user_id=user.id,
            tenant_id=payload.get("tenant_id"),
            email=email
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Token refrescado exitosamente",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "access_token": new_tokens["access_token"],
                        "token_type": new_tokens["token_type"]
                    }
                }
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={
                "message": "No se pudo refrescar el token",
                "status": 401,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/me", tags=["Authentication"])
def get_current_user_info(
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user information
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        tenant_id = request.headers.get("X-Tenant-ID")
        tenants = AuthService.get_user_tenants(db, current_user.id)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Usuario obtenido",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "user_id": current_user.id,
                        "email": current_user.email,
                        "full_name": current_user.full_name,
                        "role": current_user.role.value if current_user.role else "user",
                        "tenant_id": tenant_id,
                        "tenants": tenants
                    }
                }
            }
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail,
                "status": e.status_code,
                "error": True,
                "data": {"data": None}
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
