"""Users Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.user_service import UserService
from app.services.invitation_service import InvitationService
from app.core.security import get_current_user
from pydantic import BaseModel
from uuid import UUID


router = APIRouter()


class UserInvite(BaseModel):
    email: str
    role: str = "user"


class UserRoleUpdate(BaseModel):
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_tenant_id(request: Request):
    """Extract tenant_id from X-Tenant-ID header"""
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Tenant-ID header requerido"
        )
    try:
        return UUID(tenant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de tenant_id inválido"
        )


@router.get("/users", tags=["Users"])
def get_users(
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Get all users in tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        users = UserService.get_tenant_users(db, tenant_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Usuarios obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": users}
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
                "message": f"Error obteniendo usuarios: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.post("/users/invite", tags=["Users"])
def invite_user(
    invite_data: UserInvite,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Create user invitation
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        invitation = InvitationService.create_invitation(
            db=db,
            email=invite_data.email,
            tenant_id=tenant_id,
            invited_by=current_user.id,
            role=invite_data.role
        )
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Invitación creada exitosamente",
                "status": 201,
                "error": False,
                "data": {"data": invitation}
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
                "message": f"Error creando invitación: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.patch("/users/{user_id}/role", tags=["Users"])
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Update user role in tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        result = UserService.update_user_role(
            db=db,
            user_id=user_id,
            tenant_id=tenant_id,
            new_role=role_data.role
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Rol actualizado exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": result}
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
                "message": f"Error actualizando rol: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.delete("/users/{user_id}", tags=["Users"])
def delete_user(
    user_id: int,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Remove user from tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        result = UserService.delete_tenant_user(
            db=db,
            user_id=user_id,
            tenant_id=tenant_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Usuario removido exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": result}
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
                "message": f"Error eliminando usuario: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
