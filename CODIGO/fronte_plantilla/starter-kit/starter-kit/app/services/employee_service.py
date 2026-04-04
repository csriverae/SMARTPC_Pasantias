"""Employee Service"""
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.core.security import generate_unique_token
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime


class EmployeeService:
    """Handle employee operations"""
    
    @staticmethod
    def create_employee(db: Session, name: str, email: str, company_id: int, tenant_id: UUID):
        """Create new employee"""
        # Check if employee already exists
        existing = db.query(Employee).filter(Employee.email == email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El empleado ya existe"
            )
        
        # Generate unique QR token
        qr_token = generate_unique_token()
        
        new_employee = Employee(
            name=name,
            email=email,
            company_id=company_id,
            qr_token=qr_token,
            company_tenant_id=tenant_id
        )
        
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        
        return new_employee
    
    @staticmethod
    def get_employee_by_id(db: Session, employee_id: int, tenant_id: UUID):
        """Get employee by ID"""
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        if employee.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este empleado"
            )
        
        return employee
    
    @staticmethod
    def get_tenant_employees(db: Session, tenant_id: UUID, company_id: int = None):
        """Get employees in tenant"""
        query = db.query(Employee).filter(Employee.company_tenant_id == tenant_id)
        
        if company_id:
            query = query.filter(Employee.company_id == company_id)
        
        return query.all()
    
    @staticmethod
    def update_employee(db: Session, employee_id: int, tenant_id: UUID, **kwargs):
        """Update employee data"""
        employee = EmployeeService.get_employee_by_id(db, employee_id, tenant_id)
        
        for key, value in kwargs.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)
        
        db.commit()
        db.refresh(employee)
        
        return employee
    
    @staticmethod
    def get_employee_by_qr_token(db: Session, qr_token: str):
        """Get employee by QR token"""
        employee = db.query(Employee).filter(Employee.qr_token == qr_token).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token QR inválido"
            )
        
        return employee
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int, tenant_id: UUID):
        """Delete employee"""
        employee = EmployeeService.get_employee_by_id(db, employee_id, tenant_id)
        
        db.delete(employee)
        db.commit()
        
        return {"message": "Empleado eliminado"}
