"""
Tenant management routes
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse, TenantListResponse
from app.core.security import get_current_user
from app.api.dependencies import require_admin, get_db
from app.api.utils.response import success_response, created_response
from app.services.tenant_service import tenant_service

router = APIRouter()


@router.post(
    "/",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new tenant (Admin only)",
    tags=["Tenants"]
)
def create_tenant(
    tenant_data: TenantCreate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Create a new tenant (Admin only)"""
    tenant = tenant_service.create_tenant(db, tenant_data)
    
    return created_response(
        message="Tenant created successfully",
        data=tenant
    )


@router.get(
    "/",
    response_model=List[TenantListResponse],
    status_code=status.HTTP_200_OK,
    summary="List all tenants (Admin only)",
    tags=["Tenants"]
)
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Get list of all tenants (Admin only)"""
    tenants = tenant_service.get_all_tenants(db, skip=skip, limit=limit)
    
    return success_response(
        message=f"Retrieved {len(tenants)} tenants",
        data=tenants
    )


@router.get(
    "/{tenant_id}",
    response_model=TenantResponse,
    status_code=status.HTTP_200_OK,
    summary="Get tenant by ID (Admin only)",
    tags=["Tenants"]
)
def get_tenant_endpoint(
    tenant_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Get specific tenant (Admin only)"""
    tenant = tenant_service.get_tenant(db, tenant_id)
    
    return success_response(
        message="Tenant retrieved successfully",
        data=tenant
    )


@router.patch(
    "/{tenant_id}",
    response_model=TenantResponse,
    status_code=status.HTTP_200_OK,
    summary="Update tenant (Admin only)",
    tags=["Tenants"]
)
def update_tenant_endpoint(
    tenant_id: int,
    tenant_data: TenantUpdate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Update tenant (Admin only)"""
    tenant = tenant_service.update_tenant(db, tenant_id, tenant_data)
    
    return success_response(
        message="Tenant updated successfully",
        data=tenant
    )


@router.delete(
    "/{tenant_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete tenant (Admin only)",
    tags=["Tenants"]
)
def delete_tenant_endpoint(
    tenant_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Delete tenant (Admin only)"""
    tenant_service.delete_tenant(db, tenant_id)
    
    return success_response(
        message="Tenant deleted successfully",
        data={"tenant_id": tenant_id}
    )
