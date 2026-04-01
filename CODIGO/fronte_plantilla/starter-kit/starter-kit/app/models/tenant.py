"""
Tenant model for multi-tenant SaaS with UUID
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Tenant(Base):
    """Tenant (Company/Organization) model with UUID"""
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False, default="company")  # company, restaurant
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user_tenants = relationship("UserTenant", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.name}, type={self.type})>"
