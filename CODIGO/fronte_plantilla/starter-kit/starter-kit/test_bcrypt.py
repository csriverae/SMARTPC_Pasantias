from passlib.context import CryptContext

# Test password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

test_password = "test123"
print(f"Password: {test_password}")
print(f"Password bytes: {len(test_password.encode('utf-8'))}")

try:
    hashed = pwd_context.hash(test_password)
    print(f"✓ Hashed successfully: {hashed[:50]}...")
    
    # Test verification
    verified = pwd_context.verify(test_password, hashed)
    print(f"✓ Verification successful: {verified}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
