"""
User authentication and management routes
"""
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import logging

from app.db.session import SessionLocal
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserListResponse,
    UserLogin,
    Token,
    PasswordChangeRequest,
    UserUpdate,
)
from app.models.user import User
from app.core.security import get_current_user
from app.api.dependencies import require_admin, require_role, get_db
from app.api.utils.response import (
    success_response,
    created_response,
    not_found_response,
    unauthorized_response,
)
from app.services.user_service import user_service
from app.core.exceptions import (
    InvalidCredentials,
    ResourceNotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)

# Request models
class RefreshTokenRequest(BaseModel):
    """Request body for token refresh"""
    refresh_token: str


router = APIRouter()


# Authentication Endpoints

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    tags=["Authentication"]
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    
    - **email**: User email (must be unique)
    - **password**: Password (min 6 characters)
    - **tenant_id**: Tenant ID (required, UUID format)
    - **role**: User role (admin or employee)
    """
    user, access_token = user_service.register_user(db, user_data)
    
    return created_response(
        message="User registered successfully",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "tenant_id": str(user_data.tenant_id),
        }
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login user",
    tags=["Authentication"]
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token
    
    - **email**: User email
    - **password**: User password
    """
    user, access_token, refresh_token = user_service.login_user(db, login_data)
    
    # Get tenant_id from user's first tenant membership
    from app.models.user import UserTenant
    user_tenant = db.query(UserTenant).filter(
        UserTenant.user_id == user.id
    ).first()
    tenant_id = str(user_tenant.tenant_id) if user_tenant else None
    
    return success_response(
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "tenant_id": tenant_id,
        }
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    tags=["Authentication"]
)
def refresh_access_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    access_token, tenant_id = user_service.refresh_access_token(
        db,
        refresh_request.refresh_token
    )
    
    return success_response(
        message="Token refreshed successfully",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "tenant_id": tenant_id,
        }
    )


# User Profile Endpoints

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    tags=["Profile"]
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get authenticated user profile"""
    return success_response(
        message="User profile retrieved",
        data=current_user
    )


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user profile",
    tags=["Profile"]
)
def update_user_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update authenticated user profile"""
    updated_user = user_service.update_user_profile(
        db,
        current_user,
        update_data
    )
    
    return success_response(
        message="User profile updated successfully",
        data=updated_user
    )


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change user password",
    tags=["Profile"]
)
def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change authenticated user password"""
    user_service.change_password(db, current_user, password_data)
    
    return success_response(
        message="Password changed successfully",
        data={"user_id": current_user.id}
    )


@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Delete user account",
    tags=["Profile"]
)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete authenticated user account"""
    # Get current user's tenant from token claims
    # This requires tenant_id to be in token claims - handled by get_current_user
    # For now, get first tenant of user
    from app.models.user import UserTenant
    user_tenant = db.query(UserTenant).filter(
        UserTenant.user_id == current_user.id
    ).first()
    
    if user_tenant:
        user_service.delete_user_account(db, current_user.id, user_tenant.tenant_id)
    
    return success_response(
        message="User account deleted successfully",
        data={"user_id": str(current_user.id)}
    )


# Admin User Management Endpoints

@router.get(
    "/users",

    status_code=status.HTTP_200_OK,
    summary="List all users (Admin only)",
    tags=["Admin"]
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Get list of all users in tenant (Admin only)
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **role**: Optional filter by user role (admin or employee)
    """
    # Get current user's tenant from token claims
    from app.models.user import UserTenant
    from uuid import UUID
    
    user_tenant = db.query(UserTenant).filter(
        UserTenant.user_id == current_user.id
    ).first()
    
    if not user_tenant:
        return success_response(
            message="No users found",
            data=[]
        )
    
    tenant_id = user_tenant.tenant_id
    users = user_service.get_all_users(db, tenant_id, skip=skip, limit=limit, role=role)
    
    return success_response(
        message=f"Retrieved {len(users)} users",
        data=users
    )


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by ID (Admin only)",
    tags=["Admin"]
)
def get_user_by_id_endpoint(
    user_id: str,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Get specific user by ID (Admin only)
    
    - **user_id**: User ID to retrieve (UUID format)
    """
    from uuid import UUID
    
    try:
        user_uuid = UUID(user_id)
        user = user_service.get_user_by_id(db, user_uuid)
        
        return success_response(
            message="User retrieved successfully",
            data=user
        )
    except ValueError:
        return not_found_response("Invalid user ID format")


@router.patch(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user (Admin only)",
    tags=["Admin"]
)
def update_user_endpoint(
    user_id: str,
    update_data: UserUpdate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Update user details (Admin only)
    
    - **user_id**: User ID to update (UUID format)
    """
    from uuid import UUID
    
    try:
        user_uuid = UUID(user_id)
        
        # Get admin's tenant from token
        from app.models.user import UserTenant
        admin_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == current_user.id
        ).first()
        
        if not admin_tenant:
            return unauthorized_response("Admin has no tenant assignment")
        
        updated_user = user_service.update_user_profile_admin(
            db,
            user_uuid,
            update_data,
            admin_tenant.tenant_id
        )
        
        return success_response(
            message="User updated successfully",
            data=updated_user
        )
    except ValueError:
        return not_found_response("Invalid user ID format")


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user (Admin only)",
    tags=["Admin"]
)
def delete_user_endpoint(
    user_id: str,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Delete specific user (Admin only)
    
    - **user_id**: User ID to delete (UUID format)
    """
    from uuid import UUID
    
    try:
        user_uuid = UUID(user_id)
        
        # Get admin's tenant from token
        from app.models.user import UserTenant
        admin_tenant = db.query(UserTenant).filter(
            UserTenant.user_id == current_user.id
        ).first()
        
        if not admin_tenant:
            return unauthorized_response("Admin has no tenant assignment")
        
        user_service.delete_user_account(db, user_uuid, admin_tenant.tenant_id)
        
        return success_response(
            message="User deleted successfully",
            data={"user_id": user_id}
        )
    except ValueError:
        return not_found_response("Invalid user ID format")
