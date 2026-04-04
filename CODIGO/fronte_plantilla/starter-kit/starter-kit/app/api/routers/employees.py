"""Employees Router"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.employee_service import EmployeeService
from app.core.security import get_current_user
from pydantic import BaseModel
from uuid import UUID


router = APIRouter()


class EmployeeCreate(BaseModel):
    name: str
    email: str
    company_id: int


class EmployeeUpdate(BaseModel):
    name: str = None
    email: str = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/employees", tags=["Employees"])
def create_employee(
    employee_data: EmployeeCreate,
    current_user=Depends(get_current_user),
    tenant_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Create new employee
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        # Convert tenant_id string to UUID
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        new_employee = EmployeeService.create_employee(
            db=db,
            name=employee_data.name,
            email=employee_data.email,
            company_id=employee_data.company_id,
            tenant_id=tenant_uuid
        )
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Empleado creado exitosamente",
                "status": 201,
                "error": False,
                "data": {
                    "data": {
                        "id": new_employee.id,
                        "name": new_employee.name,
                        "email": new_employee.email,
                        "qr_token": new_employee.qr_token,
                        "company_id": new_employee.company_id
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
                "message": f"Error creando empleado: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/employees", tags=["Employees"])
def get_employees(
    current_user=Depends(get_current_user),
    tenant_id: str = None,
    company_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Get all employees for tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        employees = EmployeeService.get_tenant_employees(
            db=db,
            tenant_id=tenant_uuid,
            company_id=company_id
        )
        
        employees_data = [
            {
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "qr_token": emp.qr_token,
                "company_id": emp.company_id
            }
            for emp in employees
        ]
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Empleados obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": employees_data}
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
                "message": f"Error obteniendo empleados: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/employees/{employee_id}", tags=["Employees"])
def get_employee(
    employee_id: int,
    current_user=Depends(get_current_user),
    tenant_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Get employee by ID
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        employee = EmployeeService.get_employee_by_id(db, employee_id, tenant_uuid)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Empleado obtenido",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "id": employee.id,
                        "name": employee.name,
                        "email": employee.email,
                        "qr_token": employee.qr_token,
                        "company_id": employee.company_id
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


@router.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(
    employee_id: int,
    current_user=Depends(get_current_user),
    tenant_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Delete employee
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        result = EmployeeService.delete_employee(db, employee_id, tenant_uuid)
        
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
                "message": f"Error: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
