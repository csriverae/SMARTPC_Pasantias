"""Invitation Service for user invitations"""
from sqlalchemy.orm import Session
from app.models.user_invitation import UserInvitation, InvitationStatus
from app.models.user import User
from app.models.user_tenant import UserTenant
from app.models.tenant import Tenant
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime, timedelta, timezone
import secrets


class InvitationService:
    """Handle user invitation operations"""

    @staticmethod
    def create_invitation(db: Session, email: str, tenant_id: UUID, invited_by: int, role: str = "employee", expires_days: int = 7):
        """Create user invitation"""
        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )

        # Check if there's already a pending invitation for this email and tenant
        existing_invitation = db.query(UserInvitation).filter(
            UserInvitation.email == email,
            UserInvitation.tenant_id == str(tenant_id),
            UserInvitation.status == InvitationStatus.pending
        ).first()

        if existing_invitation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una invitación pendiente para este email en este tenant"
            )

        # Generate unique code
        code = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days)

        # Generate a temporary password for the user
        temp_password = secrets.token_urlsafe(12)  # 16 characters

        # Create invitation
        invitation = UserInvitation(
            email=email,
            code=code,
            generated_password=temp_password,  # Store the generated password
            role=role,
            tenant_id=str(tenant_id),
            invited_by=invited_by,
            status=InvitationStatus.pending,
            expires_at=expires_at
        )

        db.add(invitation)
        db.commit()
        db.refresh(invitation)

        return {
            "invitation_id": invitation.id,
            "code": code,
            "email": email,
            "generated_password": temp_password,  # Include in response for admin
            "role": role,
            "expires_at": expires_at.isoformat(),
            "tenant_id": str(tenant_id)
        }

    @staticmethod
    def accept_invitation(db: Session, code: str, full_name: str, password: str = None):
        """Accept user invitation"""
        # Find invitation
        invitation = db.query(UserInvitation).filter(
            UserInvitation.code == code,
            UserInvitation.status == InvitationStatus.pending
        ).first()

        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada o ya utilizada"
            )

        # Check expiration
        now = datetime.now(timezone.utc)
        if now > invitation.expires_at:
            invitation.status = InvitationStatus.expired
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La invitación ha expirado"
            )

        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, invitation.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )

        # Use generated password if no password provided
        final_password = password if password else invitation.generated_password
        final_full_name = full_name  # full_name is now required

        # Create user
        new_user = UserService.create_user(
            db=db,
            email=invitation.email,
            password=final_password,
            full_name=final_full_name,
            tenant_id=invitation.tenant_id,
            role=invitation.role
        )

        # Mark invitation as accepted
        invitation.status = InvitationStatus.accepted
        db.commit()

        # Get tenant info for response
        tenant = db.query(Tenant).filter(Tenant.id == invitation.tenant_id).first()

        return {
            "user_id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role.value,
            "tenant_id": str(tenant.id) if tenant else None,
            "tenant_name": tenant.name if tenant else None,
            "invitation_accepted": True,
            "generated_password_used": password is None
        }

    @staticmethod
    def get_invitation_by_code(db: Session, code: str):
        """Get invitation by code"""
        return db.query(UserInvitation).filter(UserInvitation.code == code).first()

    @staticmethod
    def get_tenant_invitations(db: Session, tenant_id: UUID):
        """Get all invitations for a tenant"""
        return db.query(UserInvitation).filter(UserInvitation.tenant_id == str(tenant_id)).all()

    @staticmethod
    def cancel_invitation(db: Session, invitation_id: int, tenant_id: UUID):
        """Cancel a pending invitation"""
        invitation = db.query(UserInvitation).filter(
            UserInvitation.id == invitation_id,
            UserInvitation.tenant_id == str(tenant_id),
            UserInvitation.status == InvitationStatus.pending
        ).first()

        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada o no puede ser cancelada"
            )

        invitation.status = InvitationStatus.expired
        db.commit()

        return {"message": "Invitación cancelada exitosamente"}

    @staticmethod
    def cleanup_expired_invitations(db: Session):
        """Mark expired invitations as expired"""
        expired_count = db.query(UserInvitation).filter(
            UserInvitation.status == InvitationStatus.pending,
            UserInvitation.expires_at < datetime.utcnow()
        ).update({"status": InvitationStatus.expired})

        db.commit()
        return expired_count
