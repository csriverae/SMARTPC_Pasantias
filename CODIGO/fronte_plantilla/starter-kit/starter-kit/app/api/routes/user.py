from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import traceback
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.crud.user import create_user, get_users, authenticate_user, get_user_by_email, delete_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    require_roles,
    verify_token,
)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user exists using get_user_by_email
        db_user = get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return create_user(db, user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = authenticate_user(db, user.email, user.password)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = {"sub": db_user.email, "role": db_user.role.value}
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")


@router.post("/refresh", response_model=Token)
def refresh_token(refresh: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = verify_token(refresh.refresh_token)
    if payload is None or payload.get("sub") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    token_data = {"sub": user.email, "role": user.role.value}
    return {
        "access_token": create_access_token(data=token_data),
        "refresh_token": create_refresh_token(data=token_data),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_endpoint(current_user=Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=List[UserResponse])
def get_users_endpoint(current_user=Depends(require_roles("admin")), db: Session = Depends(get_db)):
    try:
        return get_users(db)
    except Exception as e:
        print(f"Get users error: {e}")
        raise HTTPException(status_code=500, detail=f"Get users error: {str(e)}")


@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, current_user=Depends(require_roles("admin")), db: Session = Depends(get_db)):
    try:
        if not delete_user(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        print(f"Delete user error: {e}")
        raise HTTPException(status_code=500, detail=f"Delete user error: {str(e)}")
