from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5434
    DB_NAME: str = "smartpc"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
