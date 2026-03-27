import uuid
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("admin", "restaurant_admin", "company_admin", "employee", name="user_roles"), nullable=False, default="employee")

    restaurants = relationship("Restaurant", back_populates="owner")
    companies = relationship("Company", back_populates="owner")
    employees = relationship("Employee", back_populates="user")
    meal_logs = relationship("MealLog", back_populates="user")

