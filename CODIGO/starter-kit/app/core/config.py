from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, PostgresDsn, field_validator

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    PROJECT_NAME: str = "MesaPass v2"
    ENV: str = "development"

    # Database
    DATABASE_URL: PostgresDsn

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        return v


settings = Settings()
