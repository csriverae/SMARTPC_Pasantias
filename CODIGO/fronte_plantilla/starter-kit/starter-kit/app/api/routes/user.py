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
    - **tenant_id**: Tenant ID (required)
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    - **full_name**: Optional full name (auto-generated if not provided)
    """
    user, access_token = user_service.register_user(db, user_data)
    
    return created_response(
        message="User registered successfully",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "tenant_id": user.tenant_id,
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
    
    return success_response(
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "tenant_id": user.tenant_id,
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
    user_service.delete_user_account(db, current_user.id)
    
    return success_response(
        message="User account deleted successfully",
        data={"user_id": current_user.id}
    )


# Admin User Management Endpoints

@router.get(
    "/users",
    response_model=List[UserListResponse],
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
    Get list of all users (Admin only)
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **role**: Optional filter by user role (admin or employee)
    """
    users = user_service.get_all_users(db, skip=skip, limit=limit, tenant_id=current_user.tenant_id)
    
    return success_response(
        message=f"Retrieved {len(users)} users",
        data=users
    )


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID (Admin only)",
    tags=["Admin"]
)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Get specific user by ID (Admin only)
    
    - **user_id**: User ID to retrieve
    """
    user = user_service.get_user_by_id(db, user_id)
    
    return success_response(
        message="User retrieved successfully",
        data=user
    )


@router.patch(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user (Admin only)",
    tags=["Admin"]
)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Update user details (Admin only)
    
    - **user_id**: User ID to update
    """
    updated_user = user_service.update_user(
        db,
        user_id,
        update_data,
        current_user.tenant_id
    )
    
    return success_response(
        message="User updated successfully",
        data=updated_user
    )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user (Admin only)",
    tags=["Admin"]
)
def delete_user_endpoint(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Delete specific user (Admin only)
    
    - **user_id**: User ID to delete
    """
    user_service.delete_user_account(db, user_id, current_user.tenant_id)
    
    return success_response(
        message="User deleted successfully",
        data={"user_id": user_id}
    )
