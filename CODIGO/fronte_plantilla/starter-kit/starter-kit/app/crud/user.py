from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import User, UserTenant, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


def create_user_with_tenant(db: Session, user_data: UserCreate) -> tuple[User, UserTenant]:
    """Create a user and assign to tenant with role"""
    # Create user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    db.flush()  # Get the user ID before committing
    
    # Create user-tenant relationship
    user_tenant = UserTenant(
        user_id=db_user.id,
        tenant_id=user_data.tenant_id,
        role=user_data.role or UserRole.employee
    )
    
    db.add(user_tenant)
    db.commit()
    db.refresh(db_user)
    db.refresh(user_tenant)
    
    return db_user, user_tenant


def get_user(db: Session, user_id: UUID) -> User | None:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session) -> list[User]:
    """Get all users"""
    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_tenants(db: Session, user_id: UUID, tenant_id: UUID = None) -> list[UserTenant]:
    """Get user's tenant memberships"""
    query = db.query(UserTenant).filter(UserTenant.user_id == user_id)
    if tenant_id:
        query = query.filter(UserTenant.tenant_id == tenant_id)
    return query.all()


def get_tenant_users(db: Session, tenant_id: UUID) -> list[User]:
    """Get all users in a specific tenant"""
    return db.query(User).join(
        UserTenant, User.id == UserTenant.user_id
    ).filter(UserTenant.tenant_id == tenant_id).all()


def update_user(db: Session, user_id: UUID, update_data: dict) -> User | None:
    """Update user with provided data"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None


def update_user_role(db: Session, user_id: UUID, tenant_id: UUID, new_role: UserRole) -> UserTenant | None:
    """Update user's role in a specific tenant"""
    user_tenant = db.query(UserTenant).filter(
        UserTenant.user_id == user_id,
        UserTenant.tenant_id == tenant_id
    ).first()
    if user_tenant:
        user_tenant.role = new_role
        db.add(user_tenant)
        db.commit()
        db.refresh(user_tenant)
        return user_tenant
    return None


def delete_user(db: Session, user_id: UUID) -> bool:
    """Delete user (cascades to user_tenants)"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Authenticate user by email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def update_user_password(db: Session, user: User, new_password: str) -> User:
    """Update user password"""
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
