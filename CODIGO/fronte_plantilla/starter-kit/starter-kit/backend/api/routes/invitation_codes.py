from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.routes.auth import get_current_user, require_role
from backend.crud.invitation_code import create_invitation_code, get_invitation_codes, get_invitation_code, update_invitation_code, delete_invitation_code
from backend.schemas.invitation_code import InvitationCodeCreate, InvitationCodeUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.models.user import User

invitation_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@invitation_router.post("/", response_model=None)
def create_invitation_code_endpoint(invitation: InvitationCodeCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    updated = create_invitation_code(db, invitation)
    return api_success("Código de invitación creado", data={"invitation_code": {"id": str(updated.id), "code": updated.code, "is_used": updated.is_used}})


@invitation_router.get("/", response_model=None)
def list_invitation_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    codes = get_invitation_codes(db, skip=skip, limit=limit)
    data = [{"id": str(c.id), "code": c.code, "is_used": c.is_used} for c in codes]
    return api_success("Códigos de invitación obtenidos", data={"invitation_codes": data})


@invitation_router.get("/{code_id}", response_model=None)
def get_invitation_code_endpoint(code_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    code = get_invitation_code(db, code_id)
    if not code:
        return api_error("Código de invitación no encontrado", status=404)
    return api_success("Código de invitación encontrado", data={"invitation_code": {"id": str(code.id), "code": code.code, "is_used": code.is_used}})


@invitation_router.put("/{code_id}", response_model=None)
def update_invitation_code_endpoint(code_id: str, payload: InvitationCodeUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    code = update_invitation_code(db, code_id, payload)
    if not code:
        return api_error("Código de invitación no encontrado", status=404)
    return api_success("Código de invitación actualizado", data={"invitation_code": {"id": str(code.id), "code": code.code, "is_used": code.is_used}})


@invitation_router.delete("/{code_id}", response_model=None)
def delete_invitation_code_endpoint(code_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not delete_invitation_code(db, code_id):
        return api_error("Código de invitación no encontrado", status=404)
    return api_success("Código de invitación eliminado", data={})
