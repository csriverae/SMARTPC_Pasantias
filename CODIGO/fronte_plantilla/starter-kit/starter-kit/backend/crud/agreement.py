from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.agreement import Agreement
from backend.schemas.agreement import AgreementCreate, AgreementUpdate


def create_agreement(db: Session, agreement: AgreementCreate) -> Agreement:
    try:
        db_agreement = Agreement(
            company_id=agreement.company_id,
            restaurant_id=agreement.restaurant_id,
            terms=agreement.terms,
            signed_at=agreement.signed_at,
        )
        db.add(db_agreement)
        db.commit()
        db.refresh(db_agreement)
        return db_agreement
    except SQLAlchemyError:
        db.rollback()
        raise


def get_agreements(db: Session, skip: int = 0, limit: int = 100) -> list[Agreement]:
    return db.query(Agreement).offset(skip).limit(limit).all()


def get_agreement(db: Session, agreement_id: str) -> Agreement | None:
    return db.query(Agreement).filter(Agreement.id == agreement_id).first()


def update_agreement(db: Session, agreement_id: str, agreement: AgreementUpdate) -> Agreement | None:
    db_agreement = get_agreement(db, agreement_id)
    if not db_agreement:
        return None
    if agreement.company_id is not None:
        db_agreement.company_id = agreement.company_id
    if agreement.restaurant_id is not None:
        db_agreement.restaurant_id = agreement.restaurant_id
    if agreement.terms is not None:
        db_agreement.terms = agreement.terms
    if agreement.signed_at is not None:
        db_agreement.signed_at = agreement.signed_at
    db.commit()
    db.refresh(db_agreement)
    return db_agreement


def delete_agreement(db: Session, agreement_id: str) -> bool:
    db_agreement = get_agreement(db, agreement_id)
    if not db_agreement:
        return False
    db.delete(db_agreement)
    db.commit()
    return True
