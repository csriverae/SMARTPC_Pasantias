from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.schemas.auth import UserCreate, UserRead, Token, AuthLogin, TokenRefresh
from app.services.auth_service import AuthService
from app.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await AuthService.register_user(db, user_create.email, user_create.password, user_create.full_name, user_create.role)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return user


@router.post("/login", response_model=Token)
async def login(form_data: AuthLogin, db: AsyncSession = Depends(get_db)):
    token = await AuthService.login_user(db, form_data.email, form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return token


@router.post("/refresh", response_model=Token)
async def refresh(body: TokenRefresh):
    try:
        payload = AuthService.refresh_tokens(body.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return payload


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user
