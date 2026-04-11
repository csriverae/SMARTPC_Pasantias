#!/usr/bin/env python3
"""
Test script for user invitations system
Run this script to test the complete invitation flow
"""

import requests
import json
import sys
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_invitation_flow():
    """Test the complete invitation flow"""

    print("🚀 Testing User Invitations System")
    print("=" * 50)

    # Step 1: Register a tenant
    print("\n1. Registering tenant...")
    timestamp = int(time.time())
    register_data = {
        "email": f"admin{timestamp}@test.com",
        "password": "123456",
        "full_name": "Administrador Test",
        "tenant_name": f"Empresa Test {timestamp}"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Register response: {response.status_code}")

        if response.status_code != 201:
            print(f"❌ Register failed: {response.text}")
            return False

        register_result = response.json()
        token = register_result["data"]["data"]["access_token"]
        tenant_id = register_result["data"]["data"]["tenant_id"]
        print(f"✅ Registered successfully - Token: {token[:20]}..., Tenant ID: {tenant_id}")

    except Exception as e:
        print(f"❌ Register error: {e}")
        return False

    # Step 2: Create invitation
    print("\n2. Creating user invitation...")
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": tenant_id,
        "Content-Type": "application/json"
    }

    invite_data = {
        "email": f"invited{timestamp}@test.com",
        "role": "employee"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/users/invite", json=invite_data, headers=headers)
        print(f"Invite response: {response.status_code}")

        if response.status_code != 201:
            print(f"❌ Invite failed: {response.text}")
            return False

        invite_result = response.json()
        invitation_code = invite_result["data"]["data"]["code"]
        print(f"✅ Invitation created - Code: {invitation_code[:20]}...")

    except Exception as e:
        print(f"❌ Invite error: {e}")
        return False

    # Step 3: Accept invitation
    print("\n3. Accepting invitation...")
    accept_data = {
        "code": invitation_code,
        "password": "Invited123",
        "full_name": "Usuario Invitado"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/invitations/accept", json=accept_data)
        print(f"Accept response: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Accept failed: {response.text}")
            return False

        accept_result = response.json()
        invited_user_id = accept_result["data"]["data"]["user_id"]
        print(f"✅ Invitation accepted - User ID: {invited_user_id}")

    except Exception as e:
        print(f"❌ Accept error: {e}")
        return False

    # Step 4: Login with new user
    print("\n4. Testing login with invited user...")
    login_data = {
        "email": f"invited{timestamp}@test.com",
        "password": "Invited123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Login failed: {response.text}")
            return False

        login_result = response.json()
        invited_token = login_result["data"]["data"]["access_token"]
        print(f"✅ Invited user logged in successfully - Token: {invited_token[:20]}...")

    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

    print("\n🎉 All invitation tests passed!")
    return True

def test_database_setup():
    """Test database connection and table existence"""
    print("\n🔍 Testing database setup...")

    try:
        # Try to register (this will fail if DB is not set up, but we'll check the error)
        register_data = {
            "email": "test@test.com",
            "password": "123456",
            "full_name": "Test User",
            "tenant_name": "Test Company"
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=5)

        if response.status_code in [201, 400]:  # 400 means user exists, which is fine
            print("✅ Database connection working")
            return True
        else:
            print(f"❌ Database issue: {response.status_code} - {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

if __name__ == "__main__":
    print("User Invitations System Test")
    print("=" * 30)

    # Test database connection first
    if not test_database_setup():
        print("\n❌ Database setup failed. Please check your backend.")
        sys.exit(1)

    # Run invitation flow test
    if test_invitation_flow():
        print("\n✅ All tests passed! User invitations system is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)