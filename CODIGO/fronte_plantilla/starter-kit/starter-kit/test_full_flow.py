#!/usr/bin/env python
"""Create test tenant and test registration"""
import json
import urllib.request
import urllib.error

# First, create the tenant
tenant_url = 'http://localhost:8000/tenants'
tenant_payload = {
    'name': 'KFC',
    'slug': 'kfc'
}

print("Creating tenant...")
data = json.dumps(tenant_payload).encode('utf-8')
headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(tenant_url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        tenant_result = json.loads(response.read().decode('utf-8'))
        print(f"Tenant Created: {json.dumps(tenant_result, indent=2)}")
        tenant_id = tenant_result['data']['id']
except urllib.error.HTTPError as e:
    print(f"Tenant creation error {e.code}:")
    error_data = json.loads(e.read().decode('utf-8'))
    print(json.dumps(error_data, indent=2))
    # If tenant exists, try to list them
    print("\nListing tenants...")
    try:
        req = urllib.request.Request(f'{tenant_url}', method='GET')
        with urllib.request.urlopen(req) as response:
            tenants = json.loads(response.read().decode('utf-8'))
            print(json.dumps(tenants, indent=2))
            if tenants.get('data') and len(tenants['data']) > 0:
                tenant_id = tenants['data'][0]['id']
            else:
                tenant_id = None
    except Exception as list_e:
        print(f"Error listing: {list_e}")
        tenant_id = None
except Exception as e:
    print(f"Error: {e}")
    tenant_id = None

if tenant_id:
    print(f"\nUsing tenant_id: {tenant_id}")
    
    # Now test registration with real tenant
    reg_url = 'http://localhost:8000/auth/register'
    reg_payload = {
        'email': 'admin@kfc.com',
        'password': '123456789',
        'first_name': 'Carlos',
        'last_name': 'Rivera',
        'role': 'admin',
        'tenant_id': tenant_id
    }
    
    print("\nTesting registration...")
    data = json.dumps(reg_payload).encode('utf-8')
    
    try:
        req = urllib.request.Request(reg_url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Status: {response.status}")
            print(json.dumps(result, indent=2))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}:")
        error_data = json.loads(e.read().decode('utf-8'))
        print(json.dumps(error_data, indent=2))
