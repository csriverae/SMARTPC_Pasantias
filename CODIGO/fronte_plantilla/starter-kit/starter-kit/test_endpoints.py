#!/usr/bin/env python
"""Create test tenant and test registration with proper error handling"""
import json
import urllib.request
import urllib.error

# First check if tenant endpoint exists
print("Testing GET /tenants endpoint...")
try:
    req = urllib.request.Request('http://localhost:8000/tenants', method='GET')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"GET /tenants success: {json.dumps(result, indent=2)}")
        if result.get('data') and len(result['data']) > 0:
            tenant_id = result['data'][0]['id']
            print(f"\nFound existing tenant: {tenant_id}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)

# Now test registration with KFC tenant
tenant_id = '96261def-bc6b-422a-9592-edaaa1874662'
print(f"\nTesting registration with tenant_id: {tenant_id}")

reg_url = 'http://localhost:8000/auth/register'
reg_payload = {
    'email': 'admin@kfc.com',
    'password': '123456789',
    'first_name': 'Carlos',
    'last_name': 'Rivera',
    'role': 'admin',
    'tenant_id': tenant_id
}

data = json.dumps(reg_payload).encode('utf-8')
headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(reg_url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Status: {response.status}")
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}:")
    try:
        error_data = json.loads(e.read().decode('utf-8'))
        print(json.dumps(error_data, indent=2))
    except:
        print(e.read().decode('utf-8', errors='ignore'))
