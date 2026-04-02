from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ruc = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)  # Optional for backward compatibility

    restaurant = relationship("Restaurant", back_populates="companies")
    invitation_codes = relationship("InvitationCode", back_populates="company")
    agreements = relationship("Agreement", back_populates="company")
    employees = relationship("Employee", back_populates="company")