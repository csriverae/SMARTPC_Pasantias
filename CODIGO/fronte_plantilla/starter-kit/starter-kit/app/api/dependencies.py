"""
Dependencies for middleware and permission checks
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import verify_token, get_current_user
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.models.user import User, UserRole


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_role(*allowed_roles: UserRole):
    """Dependency factory to check if user has required role"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise AuthorizationError(
                f"This operation requires one of these roles: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user
    
    return role_checker


def require_admin():
    """Factory function to create admin role checker dependency"""
    async def admin_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != UserRole.admin:
            raise AuthorizationError("Admin access required")
        return current_user
    
    return admin_checker


async def get_current_user_from_token(authorization: str = None, db: Session = Depends(get_db)) -> User:
    """Extract and validate JWT token from Authorization header"""
    if not authorization:
        raise AuthenticationError("Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise AuthenticationError("Invalid authentication scheme")
    except ValueError:
        raise AuthenticationError("Invalid authorization header format")
    
    payload = verify_token(token)
    if payload is None or payload.get("sub") is None:
        raise AuthenticationError("Invalid or expired token")
    
    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    
    if not user:
        raise AuthenticationError("User not found")
    
    return user
