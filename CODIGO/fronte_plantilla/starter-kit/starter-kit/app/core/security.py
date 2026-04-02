from datetime import datetime, timedelta
from typing import Any, Generator

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt

from app.core.config import settings
from app.db.session import SessionLocal

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt with 72-byte limit."""
    if not isinstance(password, str) or len(password) == 0:
        raise ValueError("La contraseña debe ser una cadena no vacía")

    password_bytes = password.encode('utf-8')[:72]
    if len(password_bytes) > 72:
        raise ValueError("La contraseña es demasiado larga. Máximo 72 bytes UTF-8 permitidos por bcrypt")

    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against bcrypt hash with 72-byte limit."""
    if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
        return False

    password_bytes = plain_password.encode('utf-8')[:72]
    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
    except ValueError:
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
    payload = verify_token(token)
    if payload is None or payload.get("sub") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: str):
    def role_checker(current_user=Depends(get_current_user)):
        user_role = getattr(current_user, "role", None)
        if user_role is None or user_role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role",
            )
        return current_user

    return role_checker


def get_current_tenant(request: Request, current_user=Depends(get_current_user), db=Depends(get_db)):
    from app.crud.tenant import get_user_tenants
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        print("Tenant actual: None (no header)")
        return None  # No tenant specified, allow for backward compatibility

    # Check if user belongs to this tenant
    user_tenants = get_user_tenants(db, current_user.id)
    tenant_ids = [str(ut.tenant_id) for ut in user_tenants]
    if tenant_id not in tenant_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to the specified tenant",
        )

    print(f"Tenant actual: {tenant_id}")
    return tenant_id