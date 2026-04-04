#!/usr/bin/env python3
"""
Simple test script to validate full_name support in registration flow
"""

import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def test_registration_with_full_name():
    """Test registration with full_name field"""
    
    print("=" * 60)
    print("Full Name Registration Test")
    print("=" * 60)
    
    timestamp = int(time.time())
    
    test_cases = [
        {
            "name": "Standard full name",
            "data": {
                "email": f"user1_{timestamp}@example.com",
                "password": "TestPass123",
                "full_name": "Juan Pérez García",
                "tenant_name": f"Company 1 {timestamp}"
            }
        },
        {
            "name": "Full name with special characters",
            "data": {
                "email": f"user2_{timestamp}@example.com",
                "password": "TestPass123",
                "full_name": "María-José O'Neill",
                "tenant_name": f"Company 2 {timestamp}"
            }
        },
        {
            "name": "Full name with numbers",
            "data": {
                "email": f"user3_{timestamp}@example.com",
                "password": "TestPass123",
                "full_name": "Juan 2nd García",
                "tenant_name": f"Company 3 {timestamp}"
            }
        },
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {i}] {test_case['name']}")
        print("-" * 60)
        
        try:
            print(f"📧 Email: {test_case['data']['email']}")
            print(f"👤 Full Name: {test_case['data']['full_name']}")
            print(f"🏢 Tenant: {test_case['data']['tenant_name']}")
            
            response = requests.post(
                f"{BASE_URL}/auth/register",
                json=test_case['data'],
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                user_data = result.get("data", {}).get("data", {}).get("user", {})
                
                # Verify full_name is in response
                if user_data.get("full_name") == test_case['data']['full_name']:
                    print(f"✅ Registration successful")
                    print(f"✅ full_name correctly stored: '{user_data.get('full_name')}'")
                    print(f"✅ User ID: {user_data.get('user_id')}")
                    print(f"✅ Tenant ID: {result.get('data', {}).get('data', {}).get('tenant_id')}")
                else:
                    print(f"❌ full_name mismatch")
                    print(f"   Expected: '{test_case['data']['full_name']}'")
                    print(f"   Got: '{user_data.get('full_name')}'")
                    all_passed = False
            else:
                error_msg = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get("message", error_msg)
                except:
                    pass
                print(f"❌ Registration failed (Status {response.status_code})")
                print(f"   Error: {error_msg}")
                all_passed = False
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to backend")
            print(f"   Make sure backend is running on {BASE_URL}")
            all_passed = False
        except Exception as e:
            print(f"❌ Test error: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    print("Testing login returns full_name")
    print("=" * 60)
    
    # Test login and verify full_name is returned
    login_email = test_cases[0]['data']['email']
    login_password = test_cases[0]['data']['password']
    expected_full_name = test_cases[0]['data']['full_name']
    
    print(f"\n🔐 Logging in with: {login_email}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": login_email,
                "password": login_password
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            user_data = result.get("data", {}).get("data", {}).get("user", {})
            
            if user_data.get("full_name") == expected_full_name:
                print(f"✅ Login successful")
                print(f"✅ full_name in response: '{user_data.get('full_name')}'")
            else:
                print(f"❌ full_name mismatch in login response")
                print(f"   Expected: '{expected_full_name}'")
                print(f"   Got: '{user_data.get('full_name')}'")
                all_passed = False
        else:
            print(f"❌ Login failed (Status {response.status_code})")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        all_passed = False
    
    # Print summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests PASSED! full_name field is working correctly.")
        print("=" * 60)
        return 0
    else:
        print("❌ Some tests FAILED. Please check the implementation.")
        print("=" * 60)
        return 1


def test_validation_errors():
    """Test validation errors when full_name is missing"""
    
    print("\n" + "=" * 60)
    print("Validation Error Testing (Missing full_name)")
    print("=" * 60)
    
    timestamp = int(time.time())
    
    # Test missing full_name
    print(f"\n🧪 Testing registration WITHOUT full_name (should fail)...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": f"invalid_{timestamp}@example.com",
                "password": "TestPass123",
                "tenant_name": f"Test Company {timestamp}"
                # ← Missing full_name
            },
            timeout=10
        )
        
        if response.status_code == 422:
            result = response.json()
            print(f"✅ Correctly rejected (Status 422)")
            print(f"✅ Error message: {result.get('message')}")
            if result.get('data', {}).get('errors'):
                for error in result['data']['errors']:
                    print(f"   - {error.get('field')}: {error.get('message')}")
            return 0
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"   Expected: 422")
            return 1
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return 1


if __name__ == "__main__":
    print("\n🚀 Starting Full Name Field Tests\n")
    
    # Run main tests
    result1 = test_registration_with_full_name()
    
    # Run validation tests
    result2 = test_validation_errors()
    
    # Exit with appropriate code
    sys.exit(max(result1, result2))
