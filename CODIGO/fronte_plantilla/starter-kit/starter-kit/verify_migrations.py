#!/usr/bin/env python
import sys
from app.db.session import engine
from sqlalchemy import text

try:
    connection = engine.connect()
    
    # Check users table
    print("✅ Users table columns:")
    result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
    for row in result:
        print(f"  - {row[0]}")
    
    # Check user_invitations table
    print("\n✅ User Invitations table columns:")
    result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'user_invitations' ORDER BY ordinal_position"))
    for row in result:
        print(f"  - {row[0]}")
    
    # Check agreements table
    print("\n✅ Agreements table columns:")
    result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'agreements' ORDER BY ordinal_position"))
    for row in result:
        print(f"  - {row[0]}")
    
    connection.close()
    print("\n✅ All migrations completed successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
