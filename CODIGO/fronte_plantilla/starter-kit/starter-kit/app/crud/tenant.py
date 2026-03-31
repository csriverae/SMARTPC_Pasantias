"""
CRUD operations for Tenant model
"""
from sqlalchemy.orm import Session
from app.models.tenant import Tenant


def create_tenant(db: Session, tenant_data: dict) -> Tenant:
    """Create a new tenant"""
    tenant = Tenant(**tenant_data)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def get_tenant(db: Session, tenant_id: int) -> Tenant | None:
    """Get tenant by ID"""
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()


def get_tenant_by_slug(db: Session, slug: str) -> Tenant | None:
    """Get tenant by slug"""
    return db.query(Tenant).filter(Tenant.slug == slug).first()


def get_tenants(db: Session, skip: int = 0, limit: int = 100) -> list[Tenant]:
    """Get all tenants"""
    return db.query(Tenant).offset(skip).limit(limit).all()


def update_tenant(db: Session, tenant_id: int, update_data: dict) -> Tenant | None:
    """Update tenant"""
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return None
    for key, value in update_data.items():
        setattr(tenant, key, value)
    db.commit()
    db.refresh(tenant)
    return tenant


def delete_tenant(db: Session, tenant_id: int) -> bool:
    """Delete tenant"""
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return False
    db.delete(tenant)
    db.commit()
    return True
