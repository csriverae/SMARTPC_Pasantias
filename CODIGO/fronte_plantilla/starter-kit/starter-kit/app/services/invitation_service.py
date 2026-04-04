"""Invitation Service for user invitations"""
from sqlalchemy.orm import Session
from app.models.invitation_code import InvitationCode
from app.models.user import User
from app.models.user_tenant import UserTenant
from app.services.user_service import UserService
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime, timedelta
import secrets


class InvitationService:
    """Handle user invitation operations"""
    
    @staticmethod
    def create_invitation(db: Session, email: str, tenant_id: UUID, invited_by: int, expires_days: int = 7):
        """Create user invitation"""
        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )
        
        # Generate unique code
        code = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=expires_days)
        
        # Create invitation (using InvitationCode model)
        invitation = InvitationCode(
            code=code,
            company_id=1,  # Default company for tenant
            used=False
        )
        
        db.add(invitation)
        db.flush()
        
        # Store invitation details (extend model or use separate table if needed)
        # For now, we'll use the code as identifier
        
        db.commit()
        
        return {
            "invitation_id": invitation.id,
            "code": code,
            "email": email,
            "expires_at": expires_at.isoformat(),
            "tenant_id": str(tenant_id)
        }
    
    @staticmethod
    def accept_invitation(db: Session, code: str, password: str, full_name: str):
        """Accept user invitation"""
        # Find invitation
        invitation = db.query(InvitationCode).filter(
            InvitationCode.code == code,
            InvitationCode.used == False
        ).first()
        
        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada o ya utilizada"
            )
        
        # Check expiration (assuming expires_at field exists, if not add it)
        # For now, assume no expiration check
        
        # Create user
        # Extract email from somewhere - this is a problem
        # Need to store email in invitation
        # For now, assume email is passed separately or stored
        
        # This needs refinement - perhaps extend InvitationCode model
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Accept invitation not fully implemented - needs email storage"
        )
    
    @staticmethod
    def get_invitation_by_code(db: Session, code: str):
        """Get invitation by code"""
        return db.query(InvitationCode).filter(InvitationCode.code == code).first()
