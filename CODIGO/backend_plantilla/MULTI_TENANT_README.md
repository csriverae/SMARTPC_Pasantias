# MesaPass Multi-Tenant Implementation

## Overview
MesaPass now supports multi-tenant architecture, allowing multiple organizations (restaurants and companies) to share the same system while maintaining data isolation.

## Database Changes
New tables added:
- `tenants`: Stores tenant information (id, name, type, created_at)
- `user_tenants`: Links users to tenants with roles

New columns added to existing tables:
- `restaurants.tenant_id`
- `companies.tenant_id`
- `employees.company_tenant_id`
- `agreements.restaurant_tenant_id`, `agreements.company_tenant_id`
- `meal_logs.tenant_id`

## API Changes

### Login Response Extended
POST /auth/login now includes `tenants` array:
```json
{
  "data": {
    "data": [{
      "access_token": "...",
      "refresh_token": "...",
      "token_type": "bearer",
      "tenants": [
        {
          "tenant_id": "uuid",
          "tenant_name": "Restaurant ABC",
          "tenant_type": "restaurant",
          "role": "admin"
        }
      ]
    }]
  }
}
```

### New Endpoints
- GET /auth/tenants/me: Get user's tenants
- POST /auth/tenants/select: Select tenant (placeholder)
- GET /api/employees: Get employees filtered by tenant
- GET /api/companies: Get companies filtered by tenant

### Tenant Filtering
All protected endpoints now support optional X-Tenant-ID header for data filtering. If provided, only data belonging to that tenant is returned.

## Postman Collection
Use `Mesapass_Postman_Collection_MultiTenant.json` for testing. It includes:
- Variable `tenant_id` auto-set from login response
- Headers `Authorization: Bearer {{access_token}}` and `X-Tenant-ID: {{tenant_id}}` on protected requests

## Usage
1. Login to get tokens and tenants
2. Postman test script automatically sets `tenant_id`
3. All subsequent requests include tenant context
4. Data is filtered by tenant automatically

## Backward Compatibility
- Existing endpoints work without changes
- No tenant header = no filtering (original behavior)
- All new fields are nullable for existing data