from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
from uuid import UUID

from app.models.user import User, UserTenant, UserRole
from app.schemas.user import UserCreate, UserLogin, PasswordChangeRequest, UserUpdate
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.core.exceptions import (
    InvalidCredentials,
    EmailAlreadyExists,
    ResourceNotFoundError,
    ValidationError,
)
from app.crud.user import (
    create_user_with_tenant,
    get_user,
    get_user_by_email,
    get_users,
    get_tenant_users,
    get_user_tenants,
    update_user,
    update_user_role,
    delete_user,
    authenticate_user,
    update_user_password,
)

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user operations"""

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> tuple[User, str]:
        """
        Register a new user
        
        Args:
            db: Database session
            user_data: User creation data
        
        Returns:
            Tuple of (created user, access token)
        
        Raises:
            EmailAlreadyExists: If email is already registered
            ValidationError: If validation fails
        """
        # Check if email already exists
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise EmailAlreadyExists(user_data.email)

        # Validate unique admin per tenant
        if user_data.role == UserRole.admin:
            existing_admins = db.query(UserTenant).filter(
                UserTenant.tenant_id == user_data.tenant_id,
                UserTenant.role == UserRole.admin
            ).count()
            if existing_admins > 0:
                raise ValidationError("Only one admin allowed per tenant")

        # Create user with tenant relationship
        user, user_tenant = create_user_with_tenant(db, user_data)
        logger.info(f"User registered: {user.email} (tenant: {user_data.tenant_id}, role: {user_data.role})")

        # Generate tokens with tenant_id
        access_token = create_access_token({
            "sub": user.email,
            "tenant_id": str(user_data.tenant_id),
            "role": user_data.role.value
        })

        return user, access_token

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> tuple[User, str, Optional[str]]:
        """
        Authenticate user and generate tokens
        
        Args:
            db: Database session
            login_data: Login credentials
        
        Returns:
            Tuple of (user, access_token, refresh_token)
        
        Raises:
            InvalidCredentials: If email or password is incorrect
        """
        # Get user by email
        user = get_user_by_email(db, login_data.email)
        if not user:
            logger.warning(f"Login attempt with non-existent email: {login_data.email}")
            raise InvalidCredentials()

        # Verify password
        if not verify_password(login_data.password, user.password):
            logger.warning(f"Failed login attempt for user: {login_data.email}")
            raise InvalidCredentials()
        # Get first tenant for user
        user_tenants = get_user_tenants(db, user.id)
        if not user_tenants:
            raise InvalidCredentials()
        
        tenant_id = user_tenants[0].tenant_id
        role = user_tenants[0].role

        # Generate tokens with tenant_id
        access_token = create_access_token({
            "sub": user.email,
            "tenant_id": str(tenant_id),
            "role": role.value
        })
        refresh_token = create_refresh_token({
            "sub": user.email,
            "tenant_id": str(tenant_id),
            "role": role.value
        })

        logger.info(f"User logged in: {user.email} (tenant: {tenant_id}, role: {role})")

        return user, access_token, refresh_token

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> tuple[str, int]:
        """
        Generate new access token from refresh token
        
        Args:
            db: Database session
            refresh_token: Refresh token
        
        Returns:
            Tuple of (new access token, tenant_id)
        
        Raises:
            InvalidCredentials: If refresh token is invalid
        """
        try:
            payload = verify_token(refresh_token)
            email = payload.get("sub")
            
            if not email:
                raise InvalidCredentials("Invalid refresh token")
            
            # Verify user exists
            user = get_user_by_email(db, email)
            if not user:
                raise InvalidCredentials("User not found")
            
            # Get user's first tenant for token claims
            user_tenants = get_user_tenants(db, user.id)
            if not user_tenants:
                raise InvalidCredentials("User has no tenant assignments")
            
            tenant_id = user_tenants[0].tenant_id
            role = user_tenants[0].role
            
            # Generate new access token with tenant_id
            access_token = create_access_token({
                "sub": user.email,
                "tenant_id": str(tenant_id),
                "role": role.value
            })
            logger.info(f"Access token refreshed for user: {email} (tenant: {tenant_id})")
            
            return access_token, tenant_id
        except Exception as e:
            logger.warning(f"Failed to refresh token: {str(e)}")
            raise InvalidCredentials("Invalid or expired refresh token")

    @staticmethod
    def get_user_profile(db: Session, email: str) -> User:
        """
        Get user profile by email
        
        Args:
            db: Database session
            email: User email
        
        Returns:
            User object
        
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = get_user_by_email(db, email)
        if not user:
            raise ResourceNotFoundError(
                message="User not found",
                details={"email": email}
            )
        return user

    @staticmethod
    def change_password(
        db: Session,
        user: User,
        password_data: PasswordChangeRequest
    ) -> User:
        """
        Change user password
        
        Args:
            db: Database session
            user: User object
            password_data: Password change data
        
        Returns:
            Updated user object
        
        Raises:
            InvalidCredentials: If current password is incorrect
            ValidationError: If passwords don't match
        """
        # Verify current password
        if not verify_password(password_data.current_password, user.password):
            logger.warning(f"Failed password change attempt for user: {user.email}")
            raise InvalidCredentials()

        # Verify new passwords match (additional validation)
        if password_data.new_password != password_data.confirm_password:
            raise ValidationError("New passwords do not match")

        # Hash new password
        hashed_password = get_password_hash(password_data.new_password)

        # Update user
        user = update_user(db, user.id, {"password": hashed_password})
        logger.info(f"Password changed for user: {user.email}")

        return user

    @staticmethod
    def update_user_profile(
        db: Session,
        user: User,
        update_data: UserUpdate
    ) -> User:
        """
        Update user profile
        
        Args:
            db: Database session
            user: User object
            update_data: Update data
        
        Returns:
            Updated user object
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        
        if not update_dict:
            return user

        user = update_user(db, user.id, update_dict)
        logger.info(f"User profile updated: {user.email}")

        return user

    @staticmethod
    def get_all_users(
        db: Session,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None
    ) -> List[User]:
        """
        Get all users for a tenant with optional role filtering
        
        Args:
            db: Database session
            tenant_id: Tenant ID (required - multi-tenant)
            skip: Number of records to skip
            limit: Maximum number of records
            role: Optional role filter
        
        Returns:
            List of users in tenant
        """
        users = get_tenant_users(db, tenant_id)
        
        # Filter by role if provided
        if role:
            users = [u for u in users if u.user_tenants and any(ut.role == role for ut in u.user_tenants)]
        
        return users[skip:skip + limit]

    @staticmethod
    def update_user_profile_admin(
        db: Session,
        user_id: UUID,
        update_data: UserUpdate,
        tenant_id: UUID
    ) -> User:
        """
        Update user details (admin only, same tenant)
        
        Args:
            db: Database session
            user_id: User ID to update
            update_data: Update data
            tenant_id: Admin's tenant ID
        
        Returns:
            Updated user
        
        Raises:
            ResourceNotFoundError: If user not found or not in tenant
            ValidationError: If validation fails
        """
        # Verify user is in this tenant
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Check if user is member of tenant
        user_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id
        ).first()
        
        if not user_tenant:
            raise ResourceNotFoundError("User not found in this tenant")

        update_dict = update_data.model_dump(exclude_unset=True)
        
        if not update_dict:
            return user
        
        # If role is being updated, validate unique admin constraint
        if 'role' in update_dict and update_dict['role'] == UserRole.admin:
            existing_admin = db.query(UserTenant).filter(
                UserTenant.tenant_id == tenant_id,
                UserTenant.role == UserRole.admin,
                UserTenant.user_id != user_id
            ).first()
            if existing_admin:
                raise ValidationError("Only one admin allowed per tenant")
        
        # Update user or user_tenant based on field
        if 'role' in update_dict:
            role = update_dict.pop('role')
            update_user_role(db, user_id, tenant_id, role)
        
        if update_dict:
            user = update_user(db, user_id, update_dict)
        
        logger.info(f"User updated: {user.email}")

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID (UUID)
        
        Returns:
            User object
        
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundError("User not found")
        return user

    @staticmethod
    def delete_user_account(db: Session, user_id: UUID, tenant_id: UUID) -> bool:
        """
        Delete user account (admin only, same tenant)
        
        Args:
            db: Database session
            user_id: User ID
            tenant_id: Admin's tenant ID
        
        Returns:
            True if deletion successful
        
        Raises:
            ResourceNotFoundError: If user not found or not in tenant
        """
        # Verify user exists
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Verify user is in this tenant
        user_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id
        ).first()
        
        if not user_tenant:
            raise ResourceNotFoundError("User not found in this tenant")

        delete_user(db, user_id)
        logger.info(f"User deleted: {user.email}")

        return True


# Singleton instance
user_service = UserService()
