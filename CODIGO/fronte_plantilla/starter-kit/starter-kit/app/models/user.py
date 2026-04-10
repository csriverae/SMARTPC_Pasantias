from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    restaurant_admin = "restaurant_admin"
    company_admin = "company_admin"
    employee = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.employee)

    restaurants = relationship("Restaurant", back_populates="user")
    user_tenants = relationship("UserTenant", back_populates="user")
    sent_invitations = relationship("UserInvitation", back_populates="inviter")
    password_resets = relationship("PasswordReset", back_populates="user")
