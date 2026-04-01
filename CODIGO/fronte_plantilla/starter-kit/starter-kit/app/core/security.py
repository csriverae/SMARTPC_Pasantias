from datetime import datetime, timedelta
from typing import Any, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt

from app.core.config import settings
from app.db.session import SessionLocal

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt directly.
    This bypasses passlib's CryptContext which might have issues with certain configs.
    Bcrypt has a hard limit of 72 bytes.
    """
    # Ensure password is string
    pwd_str = str(password) if not isinstance(password, str) else password
    # Encode to UTF-8 and truncate to 72 bytes (bcrypt hard limit)
    pwd_bytes = pwd_str.encode('utf-8')[:72]
    # Decode back, ignoring incomplete multi-byte chars
    pwd_safe = pwd_bytes.decode('utf-8', errors='ignore')
    
    # Use bcrypt directly: hash with cost factor 12
    pwd_safe_bytes = pwd_safe.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pwd_safe_bytes, salt)
    
    # Return as string for storage
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash."""
    # Truncate input to 72 bytes (bcrypt limit)
    pwd_str = str(plain_password) if not isinstance(plain_password, str) else plain_password
    pwd_bytes = pwd_str.encode('utf-8')[:72]
    pwd_safe = pwd_bytes.decode('utf-8', errors='ignore')
    
    # Convert hash back to bytes and compare
    try:
        hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
        return bcrypt.checkpw(pwd_safe.encode('utf-8'), hashed_bytes)
    except Exception:
        return False


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    from app.crud.user import get_user_by_email
    from app.models.user import UserTenant
    from uuid import UUID
    
    payload = verify_token(token)
    if payload is None or payload.get("sub") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    tenant_id_str = payload.get("tenant_id")
    
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Attach tenant_id and role to user object from token for easy access in routes
    if tenant_id_str:
        try:
            user.tenant_id = UUID(tenant_id_str)
            user.role_name = payload.get("role", "employee")
        except (ValueError, TypeError):
            pass
    
    return user


def require_roles(*allowed_roles: str):
    def role_checker(token: str = Depends(oauth2_scheme)):
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
        user_role = payload.get("role", "employee")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role",
            )
        
        return payload

    return role_checker