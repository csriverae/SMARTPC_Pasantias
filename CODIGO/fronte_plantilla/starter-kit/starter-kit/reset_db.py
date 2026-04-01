from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Drop all tables
    conn.execute(text("""
        DROP TABLE IF EXISTS alembic_version CASCADE;
        DROP TABLE IF EXISTS meal_logs CASCADE;
        DROP TABLE IF EXISTS invitation_codes CASCADE;
        DROP TABLE IF EXISTS employees CASCADE;
        DROP TABLE IF EXISTS agreements CASCADE;
        DROP TABLE IF EXISTS restaurants CASCADE;
        DROP TABLE IF EXISTS companies CASCADE;
        DROP TABLE IF EXISTS user_tenants CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        DROP TABLE IF EXISTS tenants CASCADE;
    """))
    conn.commit()
    print("✓ All tables dropped successfully")
