"""Authentication Service for SaaS Multi-Tenant"""
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.tenant import Tenant
from app.models.user_tenant import UserTenant
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from fastapi import HTTPException, status


class AuthService:
    """Handle authentication operations"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña inválido"
            )
        
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña inválido"
            )
        
        return user
    
    @staticmethod
    def get_user_tenants(db: Session, user_id: int):
        """Get all tenants for a user"""
        user_tenants = db.query(UserTenant).filter(UserTenant.user_id == user_id).all()
        tenants_data = []
        
        for ut in user_tenants:
            tenant = db.query(Tenant).filter(Tenant.id == ut.tenant_id).first()
            if tenant:
                tenants_data.append({
                    "tenant_id": str(tenant.id),
                    "tenant_name": tenant.name,
                    "role": ut.role
                })
        
        return tenants_data
    
    @staticmethod
    def create_tokens(user_id: int, tenant_id: str, email: str, role: str = "user"):
        """Create access and refresh tokens"""
        access_token = create_access_token({
            "sub": email,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": role
        })
        
        refresh_token = create_refresh_token({
            "sub": email,
            "user_id": user_id,
            "tenant_id": tenant_id
        })
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    def register_owner(db: Session, email: str, password: str, full_name: str, tenant_name: str, phone: str | None = None, address: str | None = None):
        """Register a new tenant owner and create tenant automatically"""
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )

        tenant = Tenant(
            name=tenant_name,
            type="company"
        )
        db.add(tenant)
        db.flush()

        new_user = User(
            email=email,
            password=get_password_hash(password),
            full_name=full_name,
            phone=phone,
            address=address,
            role=UserRole.admin
        )
        db.add(new_user)
        db.flush()

        user_tenant = UserTenant(
            user_id=new_user.id,
            tenant_id=tenant.id,
            role="owner"
        )
        db.add(user_tenant)
        db.commit()
        db.refresh(new_user)
        db.refresh(tenant)

        return new_user, tenant, user_tenant

    @staticmethod
    def delete_user(db: Session, user_id: int, current_user_id: int, tenant_id: str):
        """Delete a user from the tenant (admin only)"""
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Check if current user is admin in the tenant
        current_user_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == current_user_id,
            UserTenant.tenant_id == tenant_id,
            UserTenant.role.in_(["admin", "owner"])
        ).first()

        if not current_user_tenant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para eliminar usuarios"
            )

        # Cannot delete yourself
        if user_id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar tu propio usuario"
            )

        # Check if target user belongs to the tenant
        target_user_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id
        ).first()

        if not target_user_tenant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no pertenece a este tenant"
            )

        # Delete user-tenant relationship first
        db.delete(target_user_tenant)

        # Check if user has other tenants
        other_tenants = db.query(UserTenant).filter(UserTenant.user_id == user_id).count()

        if other_tenants == 0:
            # User has no other tenants, delete the user completely
            # Delete related records first
            from app.models.password_reset import PasswordReset
            from app.models.user_invitation import UserInvitation
            from app.models.meal_log import MealLog
            from app.models.employee import Employee

            # Delete password resets
            db.query(PasswordReset).filter(PasswordReset.user_id == user_id).delete()

            # Delete invitations sent by this user
            db.query(UserInvitation).filter(UserInvitation.invited_by == user_id).delete()

            # Delete meal logs
            db.query(MealLog).filter(MealLog.employee_id.in_(
                db.query(Employee.id).filter(Employee.user_id == user_id)
            )).delete()

            # Delete employees
            db.query(Employee).filter(Employee.user_id == user_id).delete()

            # Finally delete the user
            db.delete(user)

        db.commit()

        return {"message": "Usuario eliminado exitosamente"}

    @staticmethod
    def register_device_session(
        db: Session,
        user_id: int,
        device_id: str,
        refresh_token: str,
        device_name: str | None = None,
        device_type: str = "mobile",
        os: str | None = None,
        os_version: str | None = None,
        app_version: str | None = None,
        device_token: str | None = None,
        expires_in_days: int = 30
    ):
        """Register a new device session for mobile app persistent login"""
        from app.crud.device_session import create_device_session
        
        # Check if device already exists
        existing_device = db.query(User).join(
            db.models.device_session.DeviceSession
        ).filter(
            db.models.device_session.DeviceSession.device_id == device_id
        ).first()
        
        # Create new device session
        device_session = create_device_session(
            db=db,
            user_id=user_id,
            device_id=device_id,
            refresh_token=refresh_token,
            device_name=device_name,
            device_type=device_type,
            os=os,
            os_version=os_version,
            app_version=app_version,
            device_token=device_token,
            expires_in_days=expires_in_days
        )
        
        return device_session

    @staticmethod
    def validate_device_session(db: Session, device_id: str) -> dict | None:
        """Validate if a device session is still active and valid"""
        from app.crud.device_session import get_device_session_by_device_id, update_device_session_last_accessed
        from app.core.security import verify_token
        
        device_session = get_device_session_by_device_id(db, device_id)
        
        if not device_session or not device_session.is_valid():
            return None
        
        # Try to verify the refresh token
        token_payload = verify_token(device_session.refresh_token)
        if not token_payload:
            return None
        
        # Update last accessed time
        update_device_session_last_accessed(db, device_id)
        
        return {
            "device_id": device_session.device_id,
            "device_name": device_session.device_name,
            "device_type": device_session.device_type,
            "user_id": device_session.user_id,
            "email": token_payload.get("sub"),
            "refresh_token": device_session.refresh_token,
            "last_accessed": device_session.last_accessed
        }

    @staticmethod
    def logout_device(db: Session, device_id: str) -> bool:
        """Logout from a specific device"""
        from app.crud.device_session import deactivate_device_session
        return deactivate_device_session(db, device_id)

    @staticmethod
    def logout_all_devices(db: Session, user_id: int) -> int:
        """Logout from all devices (password change, security issue, etc.)"""
        from app.crud.device_session import deactivate_all_user_devices
        return deactivate_all_user_devices(db, user_id)

    @staticmethod
    def get_user_devices(db: Session, user_id: int) -> list[dict]:
        """Get all active device sessions for a user"""
        from app.crud.device_session import get_user_device_sessions
        
        devices = get_user_device_sessions(db, user_id, only_active=True)
        
        return [
            {
                "device_id": d.device_id,
                "device_name": d.device_name,
                "device_type": d.device_type,
                "os": d.os,
                "os_version": d.os_version,
                "app_version": d.app_version,
                "last_accessed": d.last_accessed.isoformat(),
                "created_at": d.created_at.isoformat()
            }
            for d in devices
        ]
