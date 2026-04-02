from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    agreement_id = Column(Integer, ForeignKey("agreements.id"), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String, nullable=False)  # e.g., 'lunch', 'dinner'
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)  # Optional for backward compatibility

    employee = relationship("Employee", back_populates="meal_logs")
    agreement = relationship("Agreement", back_populates="meal_logs")