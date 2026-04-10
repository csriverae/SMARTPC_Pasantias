from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate


def create_company(db: Session, company: CompanyCreate, tenant_id: str = None) -> Company:
    # Check if RUC is already registered (if provided)
    if company.ruc:
        existing_company = db.query(Company).filter(Company.ruc == company.ruc).first()
        if existing_company:
            raise ValueError("El RUC ya está registrado")

    db_company = Company(
        name=company.name,
        ruc=company.ruc,
        tenant_id=tenant_id
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_companies(db: Session, tenant_id: str = None) -> list[Company]:
    query = db.query(Company)
    if tenant_id:
        query = query.filter(Company.tenant_id == tenant_id)
    return query.all()


def get_company_by_id(db: Session, company_id: int) -> Company | None:
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_ruc(db: Session, ruc: str) -> Company | None:
    return db.query(Company).filter(Company.ruc == ruc).first()