from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.employee import Employee
from backend.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    try:
        db_employee = Employee(
            user_id=employee.user_id,
            restaurant_id=employee.restaurant_id,
            company_id=employee.company_id,
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except SQLAlchemyError:
        db.rollback()
        raise


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> list[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: str) -> Employee | None:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def update_employee(db: Session, employee_id: str, employee: EmployeeUpdate) -> Employee | None:
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    if employee.restaurant_id is not None:
        db_employee.restaurant_id = employee.restaurant_id
    if employee.company_id is not None:
        db_employee.company_id = employee.company_id
    if employee.user_id is not None:
        db_employee.user_id = employee.user_id
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: str) -> bool:
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return False
    db.delete(db_employee)
    db.commit()
    return True
