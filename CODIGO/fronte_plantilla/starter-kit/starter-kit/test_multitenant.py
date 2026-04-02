import requests

BASE_URL = "http://localhost:8000"

# Test login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@example.com",
    "password": "admin123"
})

if response.status_code == 200:
    data = response.json()
    print("Login successful")
    access_token = data['data']['data'][0]['access_token']
    tenants = data['data']['data'][0].get('tenants', [])
    print(f"Tenants: {tenants}")

    if tenants:
        tenant_id = tenants[0]['tenant_id']
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Tenant-ID": tenant_id
        }

        # Test get tenants
        resp = requests.get(f"{BASE_URL}/auth/tenants/me", headers=headers)
        print(f"Get tenants: {resp.status_code}")

        # Test get employees
        resp = requests.get(f"{BASE_URL}/api/employees", headers=headers)
        print(f"Get employees: {resp.status_code}")
    else:
        print("No tenants found")
else:
    print(f"Login failed: {response.status_code}")