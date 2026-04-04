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
    def register_owner(db: Session, email: str, password: str, full_name: str, tenant_name: str):
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
