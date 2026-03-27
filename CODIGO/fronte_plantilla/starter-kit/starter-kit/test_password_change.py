import requests
import json

BASE_URL = "http://127.0.0.1:8000/auth"

print("=" * 60)
print("Testing Password Change Endpoint")
print("=" * 60)

# Step 1: Try to login with known user
print("\n1️⃣ Attempting login with carlos@gmail.com...")
users_to_try = [
    {"email": "carlos@gmail.com", "password": "admin123"},
    {"email": "carlos@gmail.com", "password": "carlos123"},
    {"email": "carlos@gmail.com", "password": "password"},
    {"email": "employee@gmail.com", "password": "employee123"},
]

token = None
successful_user = None

for user_attempt in users_to_try:
    login_response = requests.post(
        f"{BASE_URL}/login",
        json=user_attempt
    )
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        successful_user = user_attempt
        print(f"✅ Login successful with {user_attempt['email']}!")
        break

if not token:
    print("❌ No successful login. Creating test user...")
    # Register a new test user
    reg_response = requests.post(
        f"{BASE_URL}/register",
        json={
            "email": "testuser-pw@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "employee"
        }
    )
    if reg_response.status_code == 200:
        print("✅ Test user registered successfully")
        # Now login with this user
        login_response = requests.post(
            f"{BASE_URL}/login",
            json={
                "email": "testuser-pw@example.com",
                "password": "testpass123"
            }
        )
        if login_response.status_code == 200:
            token = login_response.json()['access_token']
            successful_user = {"email": "testuser-pw@example.com", "password": "testpass123"}
            print(f"✅ Logged in with test user!")
        else:
            print(f"❌ Login with test user failed: {login_response.text}")
            exit(1)
    else:
        print(f"❌ Registration failed: {reg_response.text}")
        exit(1)

# Step 2: Try to change password
print(f"\n2️⃣ Attempting to change password for {successful_user['email']}...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

password_change_response = requests.post(
    f"{BASE_URL}/change-password",
    headers=headers,
    json={
        "current_password": successful_user['password'],
        "new_password": "newpass123456",
        "confirm_password": "newpass123456"
    }
)

print(f"Status Code: {password_change_response.status_code}")
print(f"Response: {password_change_response.text}")

if password_change_response.status_code == 200:
    print("✅ Password change successful!")
    
    # Step 3: Try to login with new password
    print("\n3️⃣ Testing login with new password...")
    new_login_response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": successful_user['email'],
            "password": "newpass123456"
        }
    )
    
    if new_login_response.status_code == 200:
        print("✅ Login with new password successful!")
        print("\n✨ All tests passed! Password change is working correctly.")
    else:
        print(f"❌ Login with new password failed: {new_login_response.text}")
else:
    print(f"❌ Password change failed")

print("\n" + "=" * 60)
