"""Reports Service for consumption and billing"""
from sqlalchemy.orm import Session
from app.models.meal_log import MealLog
from app.models.employee import Employee
from app.models.agreement import Agreement
from uuid import UUID
from datetime import date, datetime, timedelta
from fastapi import HTTPException, status


class ReportService:
    """Handle report generation"""
    
    @staticmethod
    def get_consumption_report(db: Session, tenant_id: UUID, start_date: date = None, end_date: date = None, employee_id: int = None):
        """Generate consumption report"""
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        
        if end_date is None:
            end_date = date.today()
        
        query = db.query(MealLog).filter(
            MealLog.tenant_id == tenant_id,
            MealLog.date >= start_date,
            MealLog.date <= end_date
        )
        
        if employee_id:
            query = query.filter(MealLog.employee_id == employee_id)
        
        meal_logs = query.all()
        
        # Aggregate data
        total_consumption = sum(log.total_amount for log in meal_logs)
        total_transactions = len(meal_logs)
        
        # By employee
        by_employee = {}
        for log in meal_logs:
            emp_id = log.employee_id
            if emp_id not in by_employee:
                employee = db.query(Employee).filter(Employee.id == emp_id).first()
                by_employee[emp_id] = {
                    "employee_id": emp_id,
                    "employee_name": employee.name if employee else "Desconocido",
                    "total": 0,
                    "transactions": 0
                }
            
            by_employee[emp_id]["total"] += log.total_amount
            by_employee[emp_id]["transactions"] += 1
        
        # By meal type
        by_meal_type = {}
        for log in meal_logs:
            meal_type = log.meal_type
            if meal_type not in by_meal_type:
                by_meal_type[meal_type] = {
                    "meal_type": meal_type,
                    "total": 0,
                    "transactions": 0
                }
            
            by_meal_type[meal_type]["total"] += log.total_amount
            by_meal_type[meal_type]["transactions"] += 1
        
        # Daily breakdown
        daily_data = {}
        for log in meal_logs:
            day = str(log.date)
            if day not in daily_data:
                daily_data[day] = {
                    "date": day,
                    "total": 0,
                    "transactions": 0
                }
            
            daily_data[day]["total"] += log.total_amount
            daily_data[day]["transactions"] += 1
        
        return {
            "period": {
                "start_date": str(start_date),
                "end_date": str(end_date)
            },
            "summary": {
                "total_consumption": round(total_consumption, 2),
                "total_transactions": total_transactions,
                "average_transaction": round(total_consumption / total_transactions, 2) if total_transactions > 0 else 0
            },
            "by_employee": list(by_employee.values()),
            "by_meal_type": list(by_meal_type.values()),
            "daily": sorted(daily_data.values(), key=lambda x: x["date"])
        }
    
    @staticmethod
    def get_billing_report(db: Session, tenant_id: UUID, start_date: date = None, end_date: date = None):
        """Generate billing report"""
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        
        if end_date is None:
            end_date = date.today()
        
        # Get all meal logs in period
        meal_logs = db.query(MealLog).filter(
            MealLog.tenant_id == tenant_id,
            MealLog.date >= start_date,
            MealLog.date <= end_date
        ).all()
        
        # Group by agreement
        by_agreement = {}
        for log in meal_logs:
            agreement = db.query(Agreement).filter(Agreement.id == log.agreement_id).first()
            
            if not agreement:
                continue
            
            agr_id = agreement.id
            if agr_id not in by_agreement:
                by_agreement[agr_id] = {
                    "agreement_id": agr_id,
                    "company_id": agreement.company_id,
                    "restaurant_id": agreement.restaurant_id,
                    "total_amount": 0,
                    "transaction_count": 0,
                    "employees_count": set()
                }
            
            by_agreement[agr_id]["total_amount"] += log.total_amount
            by_agreement[agr_id]["transaction_count"] += 1
            by_agreement[agr_id]["employees_count"].add(log.employee_id)
        
        # Convert sets to counts
        for agr in by_agreement.values():
            agr["employees_count"] = len(agr["employees_count"])
        
        total_billings = sum(agr["total_amount"] for agr in by_agreement.values())
        
        return {
            "period": {
                "start_date": str(start_date),
                "end_date": str(end_date)
            },
            "summary": {
                "total_billing": round(total_billings, 2),
                "agreements_count": len(by_agreement),
                "total_employees": sum(agr["employees_count"] for agr in by_agreement.values())
            },
            "by_agreement": sorted(by_agreement.values(), key=lambda x: x["total_amount"], reverse=True)
        }
