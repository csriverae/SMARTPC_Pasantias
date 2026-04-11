import psycopg2
from psycopg2 import sql
from app.db.base import Base
from app.db.session import engine

# First, create the database if it doesn't exist
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5434,
        user="postgres",
        password="1324",
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'mesa_db';")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute("CREATE DATABASE mesa_db;")
        print("✓ Database 'mesa_db' created successfully")
    else:
        print("✓ Database 'mesa_db' already exists")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")

# Now create all tables
try:
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")
