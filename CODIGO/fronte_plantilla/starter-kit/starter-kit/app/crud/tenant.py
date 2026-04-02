from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.models.user_tenant import UserTenant


def get_user_tenants(db: Session, user_id: int):
    return db.query(UserTenant).filter(UserTenant.user_id == user_id).all()


def get_tenant_by_id(db: Session, tenant_id: str):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()