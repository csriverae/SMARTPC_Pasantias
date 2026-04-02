#!/usr/bin/env python

import requests
import json
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import create_access_token

# Setup
db = SessionLocal()
sample_user = db.query(User).first()

if sample_user:
    # Create a token
    access_token = create_access_token({"sub": sample_user.email, "tenant_id": sample_user.tenant_id})
    tenant_id = sample_user.tenant_id
    
    # Test POST /api/companies
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tenant-ID": str(tenant_id),
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": "Test Company",
        "ruc": "12345678901"
    }
    
    # Make request
    response = requests.post(
        "http://localhost:8000/api/companies",
        headers=headers,
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
else:
    print("No user found in database")

db.close()
