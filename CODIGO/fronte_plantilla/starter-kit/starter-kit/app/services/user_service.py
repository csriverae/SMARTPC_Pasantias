"""
User service layer - Business logic for user operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.models.user import User, UserRole
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
    create_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
    delete_user,
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
            raise EmailAlreadyExists(
                message=f"Email {user_data.email} is already registered",
                details={"field": "email"}
            )

        # Hash password
        hashed_password = get_password_hash(user_data.password)

        # Create user
        user_dict = {
            "tenant_id": user_data.tenant_id,
            "email": user_data.email,
            "password": hashed_password,
            "full_name": user_data.full_name,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "role": user_data.role or UserRole.employee,
        }

        user = create_user(db, user_dict)
        logger.info(f"User registered: {user.email} (tenant: {user.tenant_id})")

        # Generate tokens with tenant_id
        access_token = create_access_token({
            "sub": user.email,
            "tenant_id": user.tenant_id
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
            raise InvalidCredentials(
                message="Invalid email or password"
            )

        # Verify password
        if not verify_password(login_data.password, user.password):
            logger.warning(f"Failed login attempt for user: {login_data.email}")
            raise InvalidCredentials(
                message="Invalid email or password"
            )

        # Generate tokens with tenant_id
        access_token = create_access_token({
            "sub": user.email,
            "tenant_id": user.tenant_id
        })
        refresh_token = create_refresh_token({
            "sub": user.email,
            "tenant_id": user.tenant_id
        })

        logger.info(f"User logged in: {user.email} (tenant: {user.tenant_id})")

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
            
            # Generate new access token with tenant_id
            access_token = create_access_token({
                "sub": user.email,
                "tenant_id": user.tenant_id
            })
            logger.info(f"Access token refreshed for user: {email} (tenant: {user.tenant_id})")
            
            return access_token, user.tenant_id
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
            raise InvalidCredentials(
                message="Current password is incorrect"
            )

        # Verify new passwords match (additional validation)
        if password_data.new_password != password_data.confirm_password:
            raise ValidationError(
                message="New passwords do not match",
                details={"field": "confirm_password"}
            )

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
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None
    ) -> List[User]:
        """
        Get all users with optional filtering
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records
            role: Optional role filter
        
        Returns:
            List of users
        """
        users = get_users(db, skip=skip, limit=limit)
        
        # Filter by role if specified
        if role:
            users = [u for u in users if u.role == role]
        
        return users

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            User object
        
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundError(
                message="User not found",
                details={"user_id": user_id}
            )
        return user

    @staticmethod
    def delete_user_account(db: Session, user_id: int) -> bool:
        """
        Delete user account
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            True if deletion successful
        
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundError(
                message="User not found",
                details={"user_id": user_id}
            )

        delete_user(db, user_id)
        logger.info(f"User deleted: {user.email}")

        return True


# Singleton instance
user_service = UserService()
