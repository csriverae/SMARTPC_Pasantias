"""
Restaurant model for multi-tenant system
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Restaurant(Base):
    """Restaurant model - belongs to a tenant"""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    address = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", backref="restaurants")
    companies = relationship("Company", back_populates="restaurant")
    agreements = relationship("Agreement", back_populates="restaurant")

    def __repr__(self):
        return f"<Restaurant(id={self.id}, name={self.name}, tenant_id={self.tenant_id})>"