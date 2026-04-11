import requests

# Test registration with shorter password
try:
    response = requests.post(
        "http://localhost:8000/auth/register",
        json={
            "email": "admin@example.com",
            "password": "test123",
            "role": "admin"
        }
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Registration Success!")
        print(f"  ID: {data['id']}")
        print(f"  Email: {data['email']}")
        print(f"  Role: {data['role']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
