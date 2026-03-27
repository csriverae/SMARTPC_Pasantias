from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.invitation_code import InvitationCode
from backend.schemas.invitation_code import InvitationCodeCreate, InvitationCodeUpdate


def create_invitation_code(db: Session, code: InvitationCodeCreate) -> InvitationCode:
    try:
        db_code = InvitationCode(code=code.code, is_used=code.is_used)
        db.add(db_code)
        db.commit()
        db.refresh(db_code)
        return db_code
    except SQLAlchemyError:
        db.rollback()
        raise


def get_invitation_codes(db: Session, skip: int = 0, limit: int = 100) -> list[InvitationCode]:
    return db.query(InvitationCode).offset(skip).limit(limit).all()


def get_invitation_code(db: Session, code_id: str) -> InvitationCode | None:
    return db.query(InvitationCode).filter(InvitationCode.id == code_id).first()


def update_invitation_code(db: Session, code_id: str, code: InvitationCodeUpdate) -> InvitationCode | None:
    db_code = get_invitation_code(db, code_id)
    if not db_code:
        return None
    if code.code is not None:
        db_code.code = code.code
    if code.is_used is not None:
        db_code.is_used = code.is_used
    db.commit()
    db.refresh(db_code)
    return db_code


def delete_invitation_code(db: Session, code_id: str) -> bool:
    db_code = get_invitation_code(db, code_id)
    if not db_code:
        return False
    db.delete(db_code)
    db.commit()
    return True
