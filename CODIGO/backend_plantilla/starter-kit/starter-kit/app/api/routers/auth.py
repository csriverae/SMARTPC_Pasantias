"""Authentication Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.schemas.user import UserLogin, PasswordResetRequest, PasswordResetConfirm
from app.schemas.device import (
    DeviceInfo, DeviceSessionRequest, MobileLoginRequest, 
    DeviceValidationResponse, UserDevicesResponse
)
from app.services.auth_service import AuthService
from app.core.security import generate_unique_token, get_current_user
from app.crud.password_reset import (
    create_password_reset,
    get_password_reset_by_code,
    mark_reset_code_used
)
from app.crud.user import get_user_by_email, update_user_password
from app.crud.device_session import (
    get_device_session_by_device_id,
    update_device_token,
    get_user_device_sessions
)
import secrets
from datetime import datetime, timedelta


router = APIRouter()


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    tenant_name: str
    phone: str | None = None
    address: str | None = None


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
            full_name=register_data.full_name,
            tenant_name=register_data.tenant_name,
            phone=register_data.phone,
            address=register_data.address
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
                            "phone": user.phone,
                            "address": user.address,
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
                            "phone": user.phone,
                            "address": user.address,
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
                        "phone": current_user.phone,
                        "address": current_user.address,
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


@router.post("/forgot-password", tags=["Authentication"])
def forgot_password(request_data: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Request password reset - sends code to email
    Headers required: None
    """
    try:
        user = get_user_by_email(db, request_data.email)
        
        if not user:
            # Don't reveal if email exists or not (security best practice)
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Si el correo existe, se envió un código a tu email",
                    "status": 200,
                    "error": False,
                    "data": {"data": None}
                }
            )
        
        # Create password reset record with code
        password_reset = create_password_reset(db, request_data.email)
        
        # TODO: Send email with reset code
        print(f"📧 Password reset code for {request_data.email}: {password_reset.reset_code}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Se envió un código de recuperación a tu correo (válido 15 minutos)",
                "status": 200,
                "error": False,
                "data": {"data": {"reset_code": password_reset.reset_code}}  # En producción, no enviar el código aquí
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


@router.post("/reset-password", tags=["Authentication"])
def reset_password(reset_data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Reset password using reset code
    Headers required: None
    """
    try:
        # Verify reset code
        password_reset = get_password_reset_by_code(db, reset_data.reset_code)
        
        if not password_reset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de recuperación inválido o expirado"
            )
        
        # Verify passwords match
        if reset_data.new_password != reset_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las contraseñas no coinciden"
            )
        
        # Update user password
        user = password_reset.user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario no encontrado"
            )
        
        update_user_password(db, user, reset_data.new_password)
        
        # Mark reset code as used
        mark_reset_code_used(db, reset_data.reset_code)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Contraseña actualizada exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": None}
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


@router.delete("/users/{user_id}", tags=["User Management"])
def delete_user(
    user_id: int,
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user from the tenant (admin only)
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )

        result = AuthService.delete_user(
            db=db,
            user_id=user_id,
            current_user_id=current_user.id,
            tenant_id=tenant_id
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": result["message"],
                "status": 200,
                "error": False,
                "data": {"data": None}
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
                "message": f"Error al eliminar usuario: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


# ==================== MOBILE DEVICE SESSIONS ====================

@router.post("/mobile/login", tags=["Mobile Authentication"])
def mobile_login(credentials: MobileLoginRequest, db: Session = Depends(get_db)):
    """
    Mobile login endpoint with device persistence
    - Authenticates user with email and password
    - Registers device for automatic login on future sessions
    - Returns access token, refresh token, and device ID
    
    Headers required: None
    """
    try:
        # Authenticate user
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

        # Register device session if requested
        device_id = credentials.device_info.device_id
        if credentials.remember_device:
            AuthService.register_device_session(
                db=db,
                user_id=user.id,
                device_id=device_id,
                refresh_token=tokens["refresh_token"],
                device_name=credentials.device_info.device_name,
                device_type=credentials.device_info.device_type,
                os=credentials.device_info.os,
                os_version=credentials.device_info.os_version,
                app_version=credentials.device_info.app_version,
                device_token=credentials.device_info.device_token,
                expires_in_days=30
            )

        return JSONResponse(
            status_code=200,
            content={
                "message": "Mobile login exitoso",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"],
                        "token_type": tokens["token_type"],
                        "device_id": device_id,
                        "tenant_id": first_tenant["tenant_id"],
                        "user": {
                            "user_id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "phone": user.phone,
                            "address": user.address,
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
                "message": f"Error en mobile login: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.post("/mobile/validate-device", tags=["Mobile Authentication"])
def validate_device(device_id: str, db: Session = Depends(get_db)):
    """
    Validate device session and get automatic login token
    - Checks if device is still registered and active
    - Returns new access token if valid
    - Used for automatic login on app startup
    
    Query params: device_id
    """
    try:
        device_validation = AuthService.validate_device_session(db, device_id)
        
        if not device_validation:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Dispositivo no válido o sesión expirada",
                    "status": 401,
                    "error": True,
                    "data": {
                        "data": {
                            "is_valid": False
                        }
                    }
                }
            )

        # Get user and create new access token
        user = get_user_by_email(db, device_validation["email"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )

        new_access_token = AuthService.create_tokens(
            user_id=user.id,
            tenant_id=device_validation.get("tenant_id"),
            email=device_validation["email"],
            role="user"
        )["access_token"]

        return JSONResponse(
            status_code=200,
            content={
                "message": "Dispositivo validado - Login automático",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "is_valid": True,
                        "device_id": device_id,
                        "access_token": new_access_token,
                        "email": device_validation["email"]
                    }
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error validando dispositivo: {str(e)}",
                "status": 500,
                "error": True,
                "data": {
                    "data": {
                        "is_valid": False
                    }
                }
            }
        )


@router.post("/mobile/update-device-token", tags=["Mobile Authentication"])
def update_device_push_token(
    device_id: str,
    device_token: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update Firebase/Push notification token for a device
    - Allows device to receive push notifications
    
    Headers required: Authorization: Bearer <token>
    Query params: device_id, device_token
    """
    try:
        device_session = get_device_session_by_device_id(db, device_id)
        
        if not device_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo no encontrado"
            )

        if device_session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para actualizar este dispositivo"
            )

        updated_device = update_device_token(db, device_id, device_token)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Token de dispositivo actualizado",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "device_id": device_id,
                        "device_token": device_token
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
                "message": f"Error actualizando token: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/mobile/devices", tags=["Mobile Authentication"])
def get_user_devices(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get all registered devices for current user
    - Lists all devices where user is logged in
    - Shows device info and last access time
    
    Headers required: Authorization: Bearer <token>
    """
    try:
        devices = AuthService.get_user_devices(db, current_user.id)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Dispositivos obtenidos",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "devices": devices,
                        "total": len(devices)
                    }
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error obteniendo dispositivos: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.post("/mobile/logout-device", tags=["Mobile Authentication"])
def logout_device(device_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Logout from a specific device
    - Deactivates device session
    - User must login again on this device
    
    Headers required: Authorization: Bearer <token>
    Query params: device_id
    """
    try:
        device_session = get_device_session_by_device_id(db, device_id)
        
        if not device_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo no encontrado"
            )

        if device_session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para cerrar sesión en este dispositivo"
            )

        AuthService.logout_device(db, device_id)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Sesión cerrada en el dispositivo",
                "status": 200,
                "error": False,
                "data": {"data": None}
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
                "message": f"Error cerrando sesión: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.post("/mobile/logout-all-devices", tags=["Mobile Authentication"])
def logout_all_devices(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Logout from all devices (security measure for password change, etc.)
    - Deactivates all device sessions for the user
    - User must login again on all devices
    
    Headers required: Authorization: Bearer <token>
    """
    try:
        count = AuthService.logout_all_devices(db, current_user.id)

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Sesión cerrada en todos los dispositivos ({count} dispositivos)",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "devices_logged_out": count
                    }
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error cerrando todas las sesiones: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


# ⚠️ DEVELOPMENT ONLY - Remove in production
@router.get("/debug/password-reset-codes", tags=["Debug"])
def debug_get_password_reset_codes(db: Session = Depends(get_db)):
    """
    DEBUG ENDPOINT - Get all active password reset codes (Development only)
    Remove this endpoint in production
    """
    try:
        from app.models.password_reset import PasswordReset
        
        # Get all non-used reset codes
        reset_codes = db.query(PasswordReset).filter(
            PasswordReset.used == 0,
            PasswordReset.expires_at > datetime.utcnow()
        ).all()
        
        codes_data = []
        for code in reset_codes:
            codes_data.append({
                "email": code.email,
                "reset_code": code.reset_code,
                "expires_at": code.expires_at.isoformat() if code.expires_at else None,
                "created_at": code.created_at.isoformat() if code.created_at else None,
                "user_id": code.user_id
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Se encontraron {len(codes_data)} códigos activos",
                "status": 200,
                "error": False,
                "data": {
                    "data": codes_data
                }
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
