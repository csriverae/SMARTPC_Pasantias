#!/usr/bin/env python
"""Test registration endpoint"""
import json
import urllib.request
import urllib.error

url = 'http://localhost:8000/auth/register'
payload = {
    'email': 'admin@test.com',
    'password': '123456789',
    'first_name': 'Test',
    'last_name': 'Admin',
    'role': 'admin',
    'tenant_id': '3526aa67-2c15-42ff-9772-dca5dc86d3a0'  # Use existing KFC tenant
}

data = json.dumps(payload).encode('utf-8')
headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Status: {response.status}")
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}:")
    error_data = json.loads(e.read().decode('utf-8'))
    print(json.dumps(error_data, indent=2))
except Exception as e:
    print(f"Error: {e}")
