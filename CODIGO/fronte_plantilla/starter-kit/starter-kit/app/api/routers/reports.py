"""Reports Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.report_service import ReportService
from app.core.security import get_current_user
from uuid import UUID
from datetime import date


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


@router.get("/reports/consumption", tags=["Reports"])
def get_consumption_report(
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db),
    start_date: date = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="End date (YYYY-MM-DD)"),
    employee_id: int = Query(None, description="Filter by employee ID")
):
    """
    Get consumption report
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    Query params: start_date, end_date, employee_id (all optional)
    """
    try:
        report = ReportService.get_consumption_report(
            db=db,
            tenant_id=tenant_id,
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Reporte de consumo obtenido exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": report}
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
                "message": f"Error obteniendo reporte de consumo: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/reports/billing", tags=["Reports"])
def get_billing_report(
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db),
    start_date: date = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get billing report
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    Query params: start_date, end_date (optional)
    """
    try:
        report = ReportService.get_billing_report(
            db=db,
            tenant_id=tenant_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Reporte de facturación obtenido exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": report}
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
                "message": f"Error obteniendo reporte de facturación: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
