from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.base import Base


class InvitationCode(Base):
    __tablename__ = "invitation_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    code = Column(String, unique=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    used = Column(Boolean, default=False)

    company = relationship("Company")