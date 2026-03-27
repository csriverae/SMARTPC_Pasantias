from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.routes.auth import get_current_user, require_role
from backend.crud.employee import create_employee, get_employees, get_employee, update_employee, delete_employee
from backend.schemas.employee import EmployeeCreate, EmployeeUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.models.user import User

employee_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@employee_router.post("/", response_model=None)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    created = create_employee(db, employee)
    return api_success("Empleado creado", data={"employee": {"id": str(created.id), "user_id": str(created.user_id), "restaurant_id": str(created.restaurant_id), "company_id": str(created.company_id)}})


@employee_router.get("/", response_model=None)
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employees = get_employees(db, skip=skip, limit=limit)
    data = [{"id": str(e.id), "user_id": str(e.user_id), "restaurant_id": str(e.restaurant_id), "company_id": str(e.company_id)} for e in employees]
    return api_success("Empleados obtenidos", data={"employees": data})


@employee_router.get("/{employee_id}", response_model=None)
def get_employee_endpoint(employee_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = get_employee(db, employee_id)
    if not employee:
        return api_error("Empleado no encontrado", status=404)
    return api_success("Empleado encontrado", data={"employee": {"id": str(employee.id), "user_id": str(employee.user_id), "restaurant_id": str(employee.restaurant_id), "company_id": str(employee.company_id)}})


@employee_router.put("/{employee_id}", response_model=None)
def update_employee_endpoint(employee_id: str, payload: EmployeeUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    employee = update_employee(db, employee_id, payload)
    if not employee:
        return api_error("Empleado no encontrado", status=404)
    return api_success("Empleado actualizado", data={"employee": {"id": str(employee.id), "user_id": str(employee.user_id), "restaurant_id": str(employee.restaurant_id), "company_id": str(employee.company_id)}})


@employee_router.delete("/{employee_id}", response_model=None)
def delete_employee_endpoint(employee_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not delete_employee(db, employee_id):
        return api_error("Empleado no encontrado", status=404)
    return api_success("Empleado eliminado", data={})
