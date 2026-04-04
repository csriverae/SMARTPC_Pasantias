"""User Service for managing users"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.tenant import Tenant
from app.models.user_tenant import UserTenant
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from uuid import UUID


class UserService:
    """Handle user operations"""
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, full_name: str, tenant_id: UUID, role: str = "user"):
        """Create a new user and assign to tenant"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )
        
        # Create user
        new_user = User(
            email=email,
            password=get_password_hash(password),
            full_name=full_name,
            role=role
        )
        db.add(new_user)
        db.flush()
        
        # Assign user to tenant
        user_tenant = UserTenant(
            user_id=new_user.id,
            tenant_id=tenant_id,
            role=role
        )
        db.add(user_tenant)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_tenant_users(db: Session, tenant_id: UUID):
        """Get all users in a tenant"""
        user_tenants = db.query(UserTenant).filter(UserTenant.tenant_id == tenant_id).all()
        users = []
        
        for ut in user_tenants:
            user = db.query(User).filter(User.id == ut.user_id).first()
            if user:
                users.append({
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": ut.role
                })
        
        return users
    
    @staticmethod
    def update_user_role(db: Session, user_id: int, tenant_id: UUID, new_role: str):
        """Update user role in tenant"""
        user_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id
        ).first()
        
        if not user_tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado en este tenant"
            )
        
        user_tenant.role = new_role
        db.commit()
        db.refresh(user_tenant)
        
        return user_tenant
    
    @staticmethod
    def delete_tenant_user(db: Session, user_id: int, tenant_id: UUID):
        """Remove user from tenant"""
        user_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id
        ).first()
        
        if not user_tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado en este tenant"
            )
        
        db.delete(user_tenant)
        db.commit()
        
        return {"message": "Usuario removido del tenant"}
