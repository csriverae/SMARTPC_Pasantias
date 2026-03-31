import requests
import json

# Test registration
try:
    response = requests.post(
        "http://localhost:8000/auth/register",
        json={
            "email": "admin@example.com",
            "password": "password123",
            "role": "admin",
            "tenant_id": 1
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print(f"Parsed JSON: {response.json()}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
