from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.company import Company
from backend.schemas.company import CompanyCreate, CompanyUpdate


def create_company(db: Session, company: CompanyCreate) -> Company:
    try:
        db_company = Company(name=company.name, owner_id=company.owner_id)
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
    except SQLAlchemyError:
        db.rollback()
        raise


def get_companies(db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
    return db.query(Company).offset(skip).limit(limit).all()


def get_company(db: Session, company_id: str) -> Company | None:
    return db.query(Company).filter(Company.id == company_id).first()


def update_company(db: Session, company_id: str, company: CompanyUpdate) -> Company | None:
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    if company.name is not None:
        db_company.name = company.name
    if company.owner_id is not None:
        db_company.owner_id = company.owner_id
    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: str) -> bool:
    db_company = get_company(db, company_id)
    if not db_company:
        return False
    db.delete(db_company)
    db.commit()
    return True
