from app.db.session import engine
from sqlalchemy import text
with engine.connect() as con:
    rows = con.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")).fetchall()
    print(rows)
