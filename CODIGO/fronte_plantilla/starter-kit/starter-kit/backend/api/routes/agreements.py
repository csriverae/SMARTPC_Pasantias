from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.routes.auth import get_current_user, require_role
from backend.crud.agreement import create_agreement, get_agreements, get_agreement, update_agreement, delete_agreement
from backend.schemas.agreement import AgreementCreate, AgreementUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.models.user import User

agreement_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@agreement_router.post("/", response_model=None)
def create_agreement_endpoint(agreement: AgreementCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    created = create_agreement(db, agreement)
    return api_success("Acuerdo creado", data={"agreement": {"id": str(created.id), "company_id": str(created.company_id), "restaurant_id": str(created.restaurant_id), "terms": created.terms, "signed_at": created.signed_at.isoformat()}})


@agreement_router.get("/", response_model=None)
def list_agreements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agreements = get_agreements(db, skip=skip, limit=limit)
    data = [{"id": str(a.id), "company_id": str(a.company_id), "restaurant_id": str(a.restaurant_id), "terms": a.terms, "signed_at": a.signed_at.isoformat()} for a in agreements]
    return api_success("Acuerdos obtenidos", data={"agreements": data})


@agreement_router.get("/{agreement_id}", response_model=None)
def get_agreement_endpoint(agreement_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agreement = get_agreement(db, agreement_id)
    if not agreement:
        return api_error("Acuerdo no encontrado", status=404)
    return api_success("Acuerdo encontrado", data={"agreement": {"id": str(agreement.id), "company_id": str(agreement.company_id), "restaurant_id": str(agreement.restaurant_id), "terms": agreement.terms, "signed_at": agreement.signed_at.isoformat()}})


@agreement_router.put("/{agreement_id}", response_model=None)
def update_agreement_endpoint(agreement_id: str, payload: AgreementUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    agreement = update_agreement(db, agreement_id, payload)
    if not agreement:
        return api_error("Acuerdo no encontrado", status=404)
    return api_success("Acuerdo actualizado", data={"agreement": {"id": str(agreement.id), "company_id": str(agreement.company_id), "restaurant_id": str(agreement.restaurant_id), "terms": agreement.terms, "signed_at": agreement.signed_at.isoformat()}})


@agreement_router.delete("/{agreement_id}", response_model=None)
def delete_agreement_endpoint(agreement_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not delete_agreement(db, agreement_id):
        return api_error("Acuerdo no encontrado", status=404)
    return api_success("Acuerdo eliminado", data={})
