from sqlalchemy import text, inspect
from app.db.session import engine
from app.db.base import Base
from app.models import User, Restaurant, Company, InvitationCode, Agreement, Employee, MealLog

# Drop existing tables
print("Dropping existing tables...")
try:
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        with engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
            connection.commit()
    print("✓ Existing tables dropped")
except Exception as e:
    print(f"Error dropping tables: {e}")

# Create all tables from models
print("\nCreating tables from models...")
try:
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully")
    
    # Verify tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\nTables created: {tables}")
    
    # Check users table columns
    if 'users' in tables:
        columns = inspector.get_columns('users')
        print(f"\nUsers table columns:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
except Exception as e:
    print(f"Error creating tables: {e}")
    import traceback
    traceback.print_exc()
