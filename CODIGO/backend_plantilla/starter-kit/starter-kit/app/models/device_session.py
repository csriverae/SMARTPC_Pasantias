from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class DeviceSession(Base):
    """Model for storing mobile device sessions to avoid repeated login"""
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    device_id = Column(String, unique=True, nullable=False, index=True)  # Unique device identifier
    device_name = Column(String, nullable=True)  # e.g., iPhone 12, Samsung Galaxy
    device_type = Column(String, nullable=False)  # mobile, tablet, web
    os = Column(String, nullable=True)  # iOS, Android, Windows, etc.
    os_version = Column(String, nullable=True)
    app_version = Column(String, nullable=True)
    device_token = Column(String, nullable=True)  # Firebase token for push notifications
    
    # Session management
    refresh_token = Column(String, nullable=False)  # Encrypted refresh token
    is_active = Column(Boolean, default=True, nullable=False)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # When the device session expires
    
    # Relationship
    user = relationship("User", back_populates="device_sessions")

    def is_valid(self) -> bool:
        """Check if device session is still valid"""
        return self.is_active and datetime.utcnow() < self.expires_at
