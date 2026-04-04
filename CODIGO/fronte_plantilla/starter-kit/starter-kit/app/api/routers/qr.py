"""QR Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.qr_service import QRService
from app.core.security import get_current_user
from uuid import UUID


router = APIRouter()


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


@router.get("/employees/{employee_id}/qr", tags=["QR"])
def get_employee_qr(
    employee_id: int,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Get employee QR code as PNG image
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        qr_image_bytes = QRService.get_employee_qr_image(
            db=db,
            employee_id=employee_id,
            tenant_id=tenant_id
        )
        
        return Response(
            content=qr_image_bytes,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=employee_{employee_id}_qr.png"}
        )
    
    except HTTPException as e:
        return Response(
            content=f"Error: {e.detail}",
            status_code=e.status_code,
            media_type="text/plain"
        )
    
    except Exception as e:
        return Response(
            content=f"Error generando QR: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )
