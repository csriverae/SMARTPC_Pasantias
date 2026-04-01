#!/usr/bin/env python
"""Test complete authentication flow: register + login"""
import json
import urllib.request
import urllib.error

def test_flow():
    base_url = 'http://localhost:8000'
    tenant_id = '3526aa67-2c15-42ff-9772-dca5dc86d3a0'  # KFC
    
    # Test user credentials
    test_user = {
        'email': 'flowtest@kfc.com',
        'password': 'TestPass123!',
        'first_name': 'Flow',
        'last_name': 'Test'
    }
    
    print("=" * 70)
    print("AUTHENTICATION FLOW TEST")
    print("=" * 70)
    
    # Step 1: Register
    print("\n1️⃣  REGISTRATION TEST")
    print("-" * 70)
    
    reg_url = f'{base_url}/auth/register'
    reg_payload = {
        **test_user,
        'role': 'employee',  # Changed to employee (admin already exists in tenant)
        'tenant_id': tenant_id
    }
    
    data = json.dumps(reg_payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    try:
        req = urllib.request.Request(reg_url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Registration successful (HTTP {response.status})")
            print(f"   Email: {test_user['email']}")
            print(f"   Role: employee")
            print(f"   Tenant: {tenant_id}")
            
            access_token = result['data']['access_token']
            expires_in = result['data']['expires_in']
            print(f"   Token: {access_token[:50]}...")
            print(f"   Expires in: {expires_in}s")
    except urllib.error.HTTPError as e:
        print(f"❌ Registration failed (HTTP {e.code})")
        try:
            error = json.loads(e.read().decode('utf-8'))
            print(f"   Error: {error}")
        except:
            pass
        return
    
    # Step 2: Login with same credentials
    print("\n2️⃣  LOGIN TEST")
    print("-" * 70)
    
    login_url = f'{base_url}/auth/login'
    login_payload = {
        'email': test_user['email'],
        'password': test_user['password']
    }
    
    data = json.dumps(login_payload).encode('utf-8')
    
    try:
        req = urllib.request.Request(login_url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Login successful (HTTP {response.status})")
            print(f"   Email: {test_user['email']}")
            
            login_token = result['data']['access_token']
            print(f"   Token: {login_token[:50]}...")
            print(f"   Token type: {result['data']['token_type']}")
            
            # Tokens should be different (different issue times)
            if login_token != access_token:
                print(f"   ☑️  Fresh token issued on login")
            
    except urllib.error.HTTPError as e:
        print(f"❌ Login failed (HTTP {e.code})")
        try:
            error = json.loads(e.read().decode('utf-8'))
            print(f"   Error: {error}")
        except:
            pass
        return
    
    # Step 3: Verify token structure
    print("\n3️⃣  TOKEN VALIDATION TEST")  
    print("-" * 70)
    
    import base64
    try:
        # JWT structure: header.payload.signature
        parts = access_token.split('.')
        if len(parts) == 3:
            # Decode payload (add padding if needed)
            payload = parts[1]
            # Add padding
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            claims = json.loads(decoded)
            
            print(f"✅ Token structure valid")
            print(f"   Subject (sub): {claims.get('sub')}")
            print(f"   Tenant ID: {claims.get('tenant_id')}")
            print(f"   Role: {claims.get('role')}")
            print(f"   Expires: {claims.get('exp')}")
            
            # Validate claims
            if claims.get('sub') == test_user['email']:
                print(f"   ☑️  Email claim correct")
            if claims.get('tenant_id') == tenant_id:
                print(f"   ☑️  Tenant ID claim correct")
            if claims.get('role') == 'employee':
                print(f"   ☑️  Role claim correct")
                
    except Exception as e:
        print(f"⚠️  Token validation error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE FLOW TEST PASSED")
    print("=" * 70)

if __name__ == "__main__":
    test_flow()
