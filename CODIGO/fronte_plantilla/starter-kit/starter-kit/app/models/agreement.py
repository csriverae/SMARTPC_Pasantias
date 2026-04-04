from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Agreement(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    restaurant_tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)  # Optional for backward compatibility
    company_tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)  # Optional for backward compatibility

    company = relationship("Company", back_populates="agreements")
    restaurant = relationship("Restaurant", back_populates="agreements")
    meal_logs = relationship("MealLog", back_populates="agreement")
