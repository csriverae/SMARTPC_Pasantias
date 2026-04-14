"""Meal Logs Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.meal_log_service import MealLogService
from app.core.security import get_current_user
from pydantic import BaseModel
from uuid import UUID
from datetime import date


router = APIRouter()


class MealLogCreate(BaseModel):
    employee_id: int
    agreement_id: int
    meal_type: str
    total_amount: float


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


@router.post("/meal-logs", tags=["Meal Logs"])
def create_meal_log(
    meal_log_data: MealLogCreate,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Create meal log entry
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        new_log = MealLogService.create_meal_log(
            db=db,
            employee_id=meal_log_data.employee_id,
            agreement_id=meal_log_data.agreement_id,
            meal_type=meal_log_data.meal_type,
            total_amount=meal_log_data.total_amount,
            tenant_id=tenant_id
        )
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Registro de consumo creado exitosamente",
                "status": 201,
                "error": False,
                "data": {
                    "data": {
                        "id": new_log.id,
                        "employee_id": new_log.employee_id,
                        "agreement_id": new_log.agreement_id,
                        "date": str(new_log.date),
                        "meal_type": new_log.meal_type,
                        "total_amount": new_log.total_amount
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
                "message": f"Error creando registro de consumo: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/meal-logs", tags=["Meal Logs"])
def get_meal_logs(
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db),
    employee_id: int = None,
    start_date: date = None,
    end_date: date = None
):
    """
    Get meal logs for tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    Query params: employee_id, start_date, end_date (all optional)
    """
    try:
        meal_logs = MealLogService.get_tenant_meal_logs(
            db=db,
            tenant_id=tenant_id,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Convert to dict format
        logs_data = []
        for log in meal_logs:
            logs_data.append({
                "id": log.id,
                "employee_id": log.employee_id,
                "agreement_id": log.agreement_id,
                "date": str(log.date),
                "meal_type": log.meal_type,
                "total_amount": log.total_amount
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Registros de consumo obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": logs_data}
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
                "message": f"Error obteniendo registros de consumo: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/meal-logs/employee/{employee_id}/consumption", tags=["Meal Logs"])
def get_employee_consumption_report(
    employee_id: int,
    current_user=Depends(get_current_user),
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db),
    start_date: date = None,
    end_date: date = None
):
    """
    Get consumption report for specific employee (used after QR validation)
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    Query params: start_date, end_date (optional)
    """
    try:
        # Verify employee belongs to tenant
        from app.models.employee import Employee
        employee = db.query(Employee).filter(
            Employee.id == employee_id,
            Employee.company_tenant_id == tenant_id
        ).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado o no pertenece al tenant"
            )
        
        # Get consumption data
        consumption_data = MealLogService.get_employee_consumption_report(
            db=db,
            employee_id=employee_id,
            tenant_id=tenant_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Calculate actual period based on found records
        if consumption_data["meal_logs"]:
            dates = [log["date"] for log in consumption_data["meal_logs"]]
            actual_start_date = min(dates)
            actual_end_date = max(dates)
        else:
            actual_start_date = None
            actual_end_date = None
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Reporte de consumo obtenido exitosamente",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "employee_id": employee_id,
                        "employee_name": employee.name,
                        "employee_email": employee.email,
                        "company_id": employee.company_id,
                        "total_consumption": consumption_data["total_consumption"],
                        "total_transactions": consumption_data["total_transactions"],
                        "average_transaction": consumption_data["average_transaction"],
                        "meal_logs": consumption_data["meal_logs"],
                        "period": {
                            "start_date": actual_start_date,
                            "end_date": actual_end_date,
                            "requested_start": str(start_date) if start_date else None,
                            "requested_end": str(end_date) if end_date else None
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
                "message": f"Error obteniendo reporte de consumo: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
