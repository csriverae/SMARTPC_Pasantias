from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.routes.auth import get_current_user, require_role
from backend.crud.company import create_company, get_companies, get_company, update_company, delete_company
from backend.schemas.company import CompanyCreate, CompanyUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.models.user import User

company_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@company_router.post("/", response_model=None)
def create_company_endpoint(company: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    created = create_company(db, company)
    return api_success("Compañía creada", data={"company": {"id": str(created.id), "name": created.name, "owner_id": str(created.owner_id)}})


@company_router.get("/", response_model=None)
def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    companies = get_companies(db, skip=skip, limit=limit)
    data = [{"id": str(c.id), "name": c.name, "owner_id": str(c.owner_id)} for c in companies]
    return api_success("Compañías obtenidas", data={"companies": data})


@company_router.get("/{company_id}", response_model=None)
def get_company_endpoint(company_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company = get_company(db, company_id)
    if not company:
        return api_error("Compañía no encontrada", status=404)
    return api_success("Compañía encontrada", data={"company": {"id": str(company.id), "name": company.name, "owner_id": str(company.owner_id)}})


@company_router.put("/{company_id}", response_model=None)
def update_company_endpoint(company_id: str, payload: CompanyUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    company = update_company(db, company_id, payload)
    if not company:
        return api_error("Compañía no encontrada", status=404)
    return api_success("Compañía actualizada", data={"company": {"id": str(company.id), "name": company.name, "owner_id": str(company.owner_id)}})


@company_router.delete("/{company_id}", response_model=None)
def delete_company_endpoint(company_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not delete_company(db, company_id):
        return api_error("Compañía no encontrada", status=404)
    return api_success("Compañía eliminada", data={})
