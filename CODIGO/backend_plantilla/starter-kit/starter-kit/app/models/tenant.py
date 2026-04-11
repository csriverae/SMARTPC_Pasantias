from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "restaurant" or "company"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_tenants = relationship("UserTenant", back_populates="tenant")
    user_invitations = relationship("UserInvitation", back_populates="tenant")
