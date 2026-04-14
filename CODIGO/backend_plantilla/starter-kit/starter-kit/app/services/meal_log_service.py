"""Meal Log Service for tracking consumption"""
from sqlalchemy.orm import Session
from app.models.meal_log import MealLog
from app.models.employee import Employee
from app.models.agreement import Agreement
from fastapi import HTTPException, status
from uuid import UUID
from datetime import date, datetime, timedelta


class MealLogService:
    """Handle meal log operations"""
    
    # Daily limit per employee (in currency units)
    DAILY_LIMIT = 50.00
    
    @staticmethod
    def validate_qr_consumption(db: Session, qr_token: str, tenant_id: UUID, agreement_id: int):
        """Validate if employee can consume based on QR token"""
        from app.services.employee_service import EmployeeService
        from app.services.agreement_service import AgreementService
        
        # Get employee from QR token
        employee = EmployeeService.get_employee_by_qr_token(db, qr_token)
        
        # Verify employee belongs to tenant
        if employee.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Empleado no pertenece a este tenant"
            )
        
        # Check if agreement is active
        agreement = AgreementService.get_agreement_by_id(db, agreement_id, tenant_id)
        if not AgreementService.is_agreement_active(db, agreement_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El acuerdo no está activo"
            )
        
        # Check daily limit
        today = date.today()
        daily_logs = db.query(MealLog).filter(
            MealLog.employee_id == employee.id,
            MealLog.date == today
        ).all()
        
        daily_total = sum(log.total_amount for log in daily_logs)
        
        if daily_total >= MealLogService.DAILY_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Límite diario alcanzado: ${MealLogService.DAILY_LIMIT}"
            )
        
        return employee, agreement
    
    @staticmethod
    def create_meal_log(db: Session, employee_id: int, agreement_id: int, meal_type: str, total_amount: float, tenant_id: UUID):
        """Create meal log entry"""
        # Verify employee and agreement exist and belong to tenant
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee or employee.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
        if not agreement or agreement.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acuerdo no encontrado"
            )
        
        # Check daily limit
        today = date.today()
        daily_logs = db.query(MealLog).filter(
            MealLog.employee_id == employee_id,
            MealLog.date == today
        ).all()
        
        daily_total = sum(log.total_amount for log in daily_logs)
        
        if daily_total + total_amount > MealLogService.DAILY_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Excede el límite diario. Disponible: ${MealLogService.DAILY_LIMIT - daily_total}"
            )
        
        # Create meal log
        new_log = MealLog(
            employee_id=employee_id,
            agreement_id=agreement_id,
            date=today,
            meal_type=meal_type,
            total_amount=total_amount,
            tenant_id=tenant_id
        )
        
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        return new_log
    
    @staticmethod
    def get_meal_log_by_id(db: Session, meal_log_id: int, tenant_id: UUID):
        """Get meal log by ID"""
        meal_log = db.query(MealLog).filter(MealLog.id == meal_log_id).first()
        
        if not meal_log or meal_log.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de consumo no encontrado"
            )
        
        return meal_log
    
    @staticmethod
    def get_tenant_meal_logs(db: Session, tenant_id: UUID, employee_id: int = None, start_date: date = None, end_date: date = None):
        """Get meal logs for tenant"""
        query = db.query(MealLog).filter(MealLog.tenant_id == tenant_id)
        
        if employee_id:
            query = query.filter(MealLog.employee_id == employee_id)
        
        if start_date:
            query = query.filter(MealLog.date >= start_date)
        
        if end_date:
            query = query.filter(MealLog.date <= end_date)
        
        return query.order_by(MealLog.date.desc()).all()
    
    @staticmethod
    def get_employee_daily_limit_status(db: Session, employee_id: int, date_to_check: date = None):
        """Get employee's daily consumption limit status"""
        if date_to_check is None:
            date_to_check = date.today()
        
        daily_logs = db.query(MealLog).filter(
            MealLog.employee_id == employee_id,
            MealLog.date == date_to_check
        ).all()
        
        daily_total = sum(log.total_amount for log in daily_logs)
        remaining = max(0, MealLogService.DAILY_LIMIT - daily_total)
        
        return {
            "daily_limit": MealLogService.DAILY_LIMIT,
            "consumed": daily_total,
            "remaining": remaining,
            "exceeded": daily_total > MealLogService.DAILY_LIMIT
        }
    
    @staticmethod
    def get_employee_consumption_report(db: Session, employee_id: int, tenant_id: UUID, start_date: date = None, end_date: date = None):
        """Get consumption report for specific employee"""
        # Get meal logs for the employee within the date range
        query = db.query(MealLog).filter(
            MealLog.employee_id == employee_id,
            MealLog.tenant_id == tenant_id
        )
        
        if start_date:
            query = query.filter(MealLog.date >= start_date)
        
        if end_date:
            query = query.filter(MealLog.date <= end_date)
        
        meal_logs = query.order_by(MealLog.date.desc()).all()
        
        # Calculate totals
        total_consumption = sum(log.total_amount for log in meal_logs)
        total_transactions = len(meal_logs)
        average_transaction = total_consumption / total_transactions if total_transactions > 0 else 0
        
        # Format meal logs for response
        formatted_logs = []
        for log in meal_logs:
            formatted_logs.append({
                "id": log.id,
                "date": str(log.date),
                "meal_type": log.meal_type,
                "total_amount": log.total_amount,
                "agreement_id": log.agreement_id
            })
        
        return {
            "total_consumption": total_consumption,
            "total_transactions": total_transactions,
            "average_transaction": average_transaction,
            "meal_logs": formatted_logs
        }
