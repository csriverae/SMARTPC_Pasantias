"""Invitations Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.invitation_service import InvitationService
from app.core.security import get_current_user
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


router = APIRouter()


class InvitationCreate(BaseModel):
    email: str
    expires_days: int = 7


class InvitationAccept(BaseModel):
    code: str
    password: Optional[str] = None
    full_name: str


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


@router.post("/invitations", tags=["Invitations"])
def create_invitation(
    invite_data: InvitationCreate,
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
            expires_days=invite_data.expires_days
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


@router.post("/invitations/accept", tags=["Invitations"])
def accept_invitation(
    accept_data: InvitationAccept,
    db: Session = Depends(get_db)
):
    """
    Accept user invitation
    Headers required: None (public endpoint)
    """
    try:
        result = InvitationService.accept_invitation(
            db=db,
            code=accept_data.code,
            full_name=accept_data.full_name,
            password=accept_data.password
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Invitación aceptada exitosamente",
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
                "message": f"Error aceptando invitación: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
