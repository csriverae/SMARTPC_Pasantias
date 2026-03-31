"""
Tenant service layer - Business logic for tenant operations
"""
from sqlalchemy.orm import Session
import logging

from app.models.tenant import Tenant
from app.crud.tenant import (
    create_tenant as crud_create_tenant,
    get_tenant,
    get_tenants as crud_get_tenants,
    update_tenant as crud_update_tenant,
    delete_tenant as crud_delete_tenant,
    get_tenant_by_slug,
)
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.core.exceptions import (
    ValidationError,
    ResourceNotFoundError,
    ConflictError,
)

logger = logging.getLogger(__name__)


class TenantService:
    """Service class for tenant operations"""

    @staticmethod
    def create_tenant(db: Session, tenant_data: TenantCreate) -> Tenant:
        """
        Create a new tenant
        
        Args:
            db: Database session
            tenant_data: Tenant creation data
        
        Returns:
            Created tenant object
        
        Raises:
            ConflictError: If slug already exists
            ValidationError: If validation fails
        """
        # Check if slug already exists
        existing = get_tenant_by_slug(db, tenant_data.slug)
        if existing:
            logger.warning(f"Attempted to create tenant with existing slug: {tenant_data.slug}")
            raise ConflictError(
                message=f"Tenant with slug '{tenant_data.slug}' already exists",
                details={"field": "slug"}
            )

        # Create tenant
        tenant_dict = {
            "name": tenant_data.name,
            "slug": tenant_data.slug,
            "description": tenant_data.description,
            "is_active": 1,
        }

        tenant = crud_create_tenant(db, tenant_dict)
        logger.info(f"Tenant created: {tenant.slug} (ID: {tenant.id})")

        return tenant

    @staticmethod
    def get_tenant(db: Session, tenant_id: int) -> Tenant:
        """
        Get tenant by ID
        
        Args:
            db: Database session
            tenant_id: Tenant ID
        
        Returns:
            Tenant object
        
        Raises:
            ResourceNotFoundError: If tenant not found
        """
        tenant = get_tenant(db, tenant_id)
        if not tenant:
            raise ResourceNotFoundError(
                message="Tenant not found",
                details={"tenant_id": tenant_id}
            )
        return tenant

    @staticmethod
    def get_all_tenants(db: Session, skip: int = 0, limit: int = 100) -> list[Tenant]:
        """
        Get all tenants
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records
        
        Returns:
            List of tenants
        """
        return crud_get_tenants(db, skip=skip, limit=limit)

    @staticmethod
    def update_tenant(db: Session, tenant_id: int, update_data: TenantUpdate) -> Tenant:
        """
        Update tenant
        
        Args:
            db: Database session
            tenant_id: Tenant ID
            update_data: Update data
        
        Returns:
            Updated tenant object
        
        Raises:
            ResourceNotFoundError: If tenant not found
        """
        tenant = get_tenant(db, tenant_id)
        if not tenant:
            raise ResourceNotFoundError(
                message="Tenant not found",
                details={"tenant_id": tenant_id}
            )

        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return tenant

        updated_tenant = crud_update_tenant(db, tenant_id, update_dict)
        logger.info(f"Tenant updated: {tenant.slug}")

        return updated_tenant

    @staticmethod
    def delete_tenant(db: Session, tenant_id: int) -> bool:
        """
        Delete tenant
        
        Args:
            db: Database session
            tenant_id: Tenant ID
        
        Returns:
            True if deletion successful
        
        Raises:
            ResourceNotFoundError: If tenant not found
        """
        tenant = get_tenant(db, tenant_id)
        if not tenant:
            raise ResourceNotFoundError(
                message="Tenant not found",
                details={"tenant_id": tenant_id}
            )

        crud_delete_tenant(db, tenant_id)
        logger.info(f"Tenant deleted: {tenant.slug}")

        return True


# Singleton instance
tenant_service = TenantService()
