"""Agreements Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.agreement_service import AgreementService
from app.core.security import get_current_user
from pydantic import BaseModel
from uuid import UUID
from datetime import date


router = APIRouter()


class AgreementCreate(BaseModel):
    company_id: int
    restaurant_id: int
    start_date: date
    end_date: date


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


@router.post("/agreements", tags=["Agreements"])
def create_agreement(
    agreement_data: AgreementCreate,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Create new agreement
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        new_agreement = AgreementService.create_agreement(
            db=db,
            company_id=agreement_data.company_id,
            restaurant_id=agreement_data.restaurant_id,
            start_date=agreement_data.start_date,
            end_date=agreement_data.end_date,
            tenant_id=tenant_id
        )
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Acuerdo creado exitosamente",
                "status": 201,
                "error": False,
                "data": {
                    "data": {
                        "id": new_agreement.id,
                        "company_id": new_agreement.company_id,
                        "restaurant_id": new_agreement.restaurant_id,
                        "start_date": str(new_agreement.start_date),
                        "end_date": str(new_agreement.end_date)
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
                "message": f"Error creando acuerdo: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/agreements", tags=["Agreements"])
def get_agreements(
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db),
    company_id: int = None
):
    """
    Get agreements for tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    Query params: company_id (optional)
    """
    try:
        agreements = AgreementService.get_tenant_agreements(
            db=db,
            tenant_id=tenant_id,
            company_id=company_id
        )
        
        # Convert to dict format
        agreements_data = []
        for agr in agreements:
            agreements_data.append({
                "id": agr.id,
                "company_id": agr.company_id,
                "restaurant_id": agr.restaurant_id,
                "start_date": str(agr.start_date),
                "end_date": str(agr.end_date),
                "is_active": AgreementService.is_agreement_active(db, agr.id)
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Acuerdos obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": agreements_data}
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
                "message": f"Error obteniendo acuerdos: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
