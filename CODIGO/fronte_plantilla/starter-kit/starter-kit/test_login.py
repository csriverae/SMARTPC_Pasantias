import requests

# Test login
try:
    response = requests.post(
        "http://localhost:8000/auth/login",
        json={
            "email": "admin@example.com",
            "password": "test123"
        }
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Login Success!")
        print(f"  Token Type: {data['token_type']}")
        print(f"  Access Token: {data['access_token'][:50]}...")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
