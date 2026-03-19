from datetime import timedelta

from app.core.security import create_access_token, create_refresh_token, verify_token
from app.services.users import UserService
from app.models.user import User


class AuthService:
    @staticmethod
    async def register_user(db, email: str, password: str, full_name: str | None, role: str = "employee") -> User:
        existing = await UserService.get_by_email(db, email)
        if existing:
            raise ValueError("Email already registered")
        return await UserService.create_user(db, email, password, full_name, role)

    @staticmethod
    async def login_user(db, email: str, password: str):
        user = await UserService.get_by_email(db, email)
        if not user or not UserService.authenticate_user(user, password):
            return None

        token_data = {"sub": str(user.id), "role": user.role.value}
        access_token = create_access_token(token_data, expires_delta=timedelta(minutes=15))
        refresh_token = create_refresh_token(token_data, expires_delta=timedelta(days=7))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def refresh_tokens(refresh_token: str):
        payload = verify_token(refresh_token, token_type="refresh")
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid refresh token")

        token_data = {"sub": user_id, "role": payload.get("role")}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
