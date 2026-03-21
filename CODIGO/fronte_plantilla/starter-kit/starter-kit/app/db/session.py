from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexión fija (segunda DB solicitada): mesa_db
DATABASE_URL = "postgresql://postgres:1234@localhost:5434/mesa_db"
print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"client_encoding": "utf8"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
