"""
Script to check all tables in PostgreSQL 'public' schema
Compatible with FastAPI + SQLAlchemy
"""

from app.db.session import engine
from sqlalchemy import text

def check_tables():
    """List all tables in the 'public' schema"""
    try:
        with engine.connect() as con:
            # Query to get all table names from public schema
            query = text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;")
            result = con.execute(query)
            tables = [row[0] for row in result]
            
            print(f"\n✅ Connected to database successfully")
            print(f"📊 Tables found in 'public' schema: {len(tables)}\n")
            
            if tables:
                print("Tables:")
                for table in tables:
                    print(f"  ✓ {table}")
            else:
                print("  (No tables found)")
            
            print()
            return tables
    
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return []

if __name__ == "__main__":
    check_tables()
