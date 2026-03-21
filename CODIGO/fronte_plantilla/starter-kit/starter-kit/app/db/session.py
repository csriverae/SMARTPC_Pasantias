from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.base import Base

settings = Settings()

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
print("DATABASE_URL:", DATABASE_URL)

# Fallback directo para descartar errores de carga .env
DATABASE_URL = "postgresql://postgres:1234@localhost:5434/smartpc_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas automáticamente al iniciar
Base.metadata.create_all(bind=engine)
