# Full Name Field Refactoring - Complete Documentation

## Overview

The authentication and user creation flow has been refactored to properly support and persist the **full_name** field across the entire system. This document outlines all changes made and how to use the updated system.

## Changes Made

### 1. Pydantic Schemas (app/schemas/user.py)

**Status**: ✅ Already Implemented

```python
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    role: UserRole | None = None
```

**Updates Made**:
- `full_name` is properly defined (optional with auto-build from first_name/last_name)

```python
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    full_name: str | None = None
    role: UserRole
```

**Updates Made**:
- `full_name` is included in response schema

### 2. Auth Router Schema (app/api/routers/auth.py)

**Status**: ✅ Updated in this refactoring

**Before**:
```python
class UserRegister(BaseModel):
    email: str
    password: str
    tenant_name: str
```

**After**:
```python
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str  # ← NOW REQUIRED
    tenant_name: str
```

### 3. Auth Service (app/services/auth_service.py)

**Status**: ✅ Updated in this refactoring

**Before**:
```python
def register_owner(db: Session, email: str, password: str, tenant_name: str):
    ...
    new_user = User(
        email=email,
        password=get_password_hash(password),
        full_name=None,  # ← HARDCODED TO NONE
        role=UserRole.admin
    )
```

**After**:
```python
def register_owner(db: Session, email: str, password: str, full_name: str, tenant_name: str):
    ...
    new_user = User(
        email=email,
        password=get_password_hash(password),
        full_name=full_name,  # ← NOW USES PARAMETER
        role=UserRole.admin
    )
```

### 4. Register Endpoint (app/api/routers/auth.py)

**Status**: ✅ Updated in this refactoring

**Before**:
```python
user, tenant, user_tenant = AuthService.register_owner(
    db=db,
    email=register_data.email,
    password=register_data.password,
    tenant_name=register_data.tenant_name
)
```

**After**:
```python
user, tenant, user_tenant = AuthService.register_owner(
    db=db,
    email=register_data.email,
    password=register_data.password,
    full_name=register_data.full_name,  # ← NOW PASSED
    tenant_name=register_data.tenant_name
)
```

### 5. SQLAlchemy User Model (app/models/user.py)

**Status**: ✅ Already Implemented

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)  # ✅ Already exists
    role = Column(Enum(UserRole), nullable=False, default=UserRole.employee)
```

### 6. User Service (app/services/user_service.py)

**Status**: ✅ Already Implemented

```python
@staticmethod
def create_user(db: Session, email: str, password: str, full_name: str, tenant_id: UUID, role: str = "user"):
    """Create a new user and assign to tenant"""
    new_user = User(
        email=email,
        password=get_password_hash(password),
        full_name=full_name,  # ✅ Already uses parameter
        role=role
    )
    ...
```

### 7. Response Endpoints

All endpoints now properly return full_name:

#### POST /auth/register
```json
{
  "message": "Registro exitoso",
  "status": 201,
  "error": false,
  "data": {
    "data": {
      "access_token": "...",
      "refresh_token": "...",
      "token_type": "bearer",
      "tenant_id": "...",
      "user": {
        "user_id": 1,
        "email": "admin@example.com",
        "full_name": "Juan Pérez",
        "tenant_role": "owner"
      }
    }
  }
}
```

#### POST /auth/login
```json
{
  "message": "Login exitoso",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "access_token": "...",
      "refresh_token": "...",
      "token_type": "bearer",
      "tenant_id": "...",
      "user": {
        "user_id": 1,
        "email": "admin@example.com",
        "full_name": "Juan Pérez",
        "tenant_role": "owner",
        "tenants": [...]
      }
    }
  }
}
```

#### GET /auth/me
```json
{
  "message": "Usuario obtenido",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "user_id": 1,
      "email": "admin@example.com",
      "full_name": "Juan Pérez",
      "role": "admin",
      "tenant_id": "...",
      "tenants": [...]
    }
  }
}
```

## API Usage Examples

### 1. Register with Full Name

**Request**:
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "SecurePassword123",
  "full_name": "Juan Pérez",
  "tenant_name": "Mi Empresa"
}
```

**Response** (201 Created):
```json
{
  "message": "Registro exitoso",
  "status": 201,
  "error": false,
  "data": {
    "data": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "token_type": "bearer",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
      "user": {
        "user_id": 1,
        "email": "admin@example.com",
        "full_name": "Juan Pérez",
        "tenant_role": "owner"
      }
    }
  }
}
```

### 2. Invite User with Full Name (Invitation System)

**Request**:
```bash
POST /api/users/invite
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}
Content-Type: application/json

{
  "email": "newuser@example.com",
  "role": "employee"
}
```

**Response** (201 Created):
```json
{
  "message": "Invitación creada",
  "data": {
    "data": {
      "invitation_id": 15,
      "code": "mcZOL1yUsWRJaj22Q7V2...",
      "email": "newuser@example.com",
      "role": "employee",
      "expires_at": "2024-04-11T08:30:45.123456",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

### 3. Accept Invitation with Full Name

**Request**:
```bash
POST /api/invitations/accept
Content-Type: application/json

{
  "code": "mcZOL1yUsWRJaj22Q7V2...",
  "password": "NewPassword123",
  "full_name": "María García"
}
```

**Response** (200 OK):
```json
{
  "message": "Invitación aceptada",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "user_id": 2,
      "email": "newuser@example.com",
      "full_name": "María García",
      "message": "Bienvenido a {{tenant_name}}"
    }
  }
}
```

### 4. Login with Full Name Returned

**Request**:
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "SecurePassword123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login exitoso",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "token_type": "bearer",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
      "user": {
        "user_id": 1,
        "email": "admin@example.com",
        "full_name": "Juan Pérez",
        "tenant_role": "owner",
        "tenants": [
          {
            "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
            "tenant_name": "Mi Empresa",
            "role": "owner"
          }
        ]
      }
    }
  }
}
```

### 5. Get Current User with Full Name

**Request**:
```bash
GET /auth/me
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}
```

**Response** (200 OK):
```json
{
  "message": "Usuario obtenido",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "user_id": 1,
      "email": "admin@example.com",
      "full_name": "Juan Pérez",
      "role": "admin",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
      "tenants": [
        {
          "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
          "tenant_name": "Mi Empresa",
          "role": "owner"
        }
      ]
    }
  }
}
```

## Validation Rules

### full_name Field

- **Type**: String (required in registration, optional in user model)
- **Length**: No specific limit (inherited from VARCHAR database column)
- **Format**: Can contain spaces, letters, numbers, and special characters
- **Required in**:
  - ✅ `POST /auth/register` (REQUIRED)
  - ✅ `POST /api/invitations/accept` (REQUIRED)
- **Optional in**:
  - User updates (if implementing user profile updates)

### In Schemas

```python
class UserCreate(BaseModel):
    full_name: str | None = None  # Optional, can be auto-built from first_name + last_name

class UserRegister(BaseModel):
    full_name: str  # REQUIRED in registration

class UserResponse(BaseModel):
    full_name: str | None = None  # May be None if not provided
```

## Testing

### Test Registration Flow

```bash
# Run the complete test suite
python test_invitations.py
```

**Test Coverage**:
- ✅ Database connection
- ✅ User registration with full_name
- ✅ Tenant creation
- ✅ User invitation creation
- ✅ Invitation acceptance with invited user's full_name
- ✅ Login with full_name returned
- ✅ Get current user with full_name

### Quick Test with curl

```bash
# Register a new user with full_name
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "full_name": "Test User Name",
    "tenant_name": "Test Company"
  }'
```

### Postman Collection

Use the existing Postman collection `Proyecto_MESAPASS_COMPLETE.json`:

1. **Auth -> Register** - Now include `full_name` in body
2. **Auth -> Login** - Response includes `full_name`
3. **Auth -> Get Current User** - Response includes `full_name`

## Backward Compatibility

⚠️ **Breaking Change**: The `full_name` field is now **REQUIRED** in the registration endpoint.

### Migration Guide for Existing Clients

If you have existing code calling `/auth/register`, add the `full_name` field:

**Before** (Will fail with 422):
```json
{
  "email": "user@example.com",
  "password": "password123",
  "tenant_name": "My Company"
}
```

**After** (Works correctly):
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "User Full Name",
  "tenant_name": "My Company"
}
```

## Data Storage

### Database Column

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    full_name VARCHAR NULL,  -- Stores the full name
    role VARCHAR NOT NULL DEFAULT 'employee',
    ...
);

-- Sample data
INSERT INTO users (email, password, full_name, role) VALUES
('admin@example.com', '$2b$12$...', 'Juan Pérez', 'admin'),
('user@example.com', '$2b$12$...', 'María García', 'employee');
```

## Security Considerations

- ✅ `full_name` is not used in authentication (only email + password)
- ✅ `full_name` is not sensitive data (can be displayed safely)
- ✅ `full_name` is always returned in authenticated responses
- ✅ No PII concerns due to business nature of the field
- ✅ Standard SQLAlchemy ORM protection against SQL injection

## Features Maintained

All existing features remain intact:

- ✅ Multi-tenant architecture
- ✅ JWT token generation
- ✅ Role-based access control
- ✅ Refresh token functionality
- ✅ User invitation system
- ✅ Email validation
- ✅ Password hashing with bcrypt
- ✅ Database connection pool

## Summary of Changes

| Component | Before | After | Status |
|-----------|--------|-------|--------|
| UserRegister schema | No full_name | full_name (required) | ✅ Updated |
| register_owner method | hardcoded None | Uses parameter | ✅ Updated |
| Register endpoint | Not passed | Passed to service | ✅ Updated |
| Database storage | NULL | Actual value | ✅ Working |
| /auth/register response | No full_name | Includes full_name | ✅ Working |
| /auth/login response | No full_name | Includes full_name | ✅ Working |
| /auth/me response | No full_name | Includes full_name | ✅ Working |
| User model | Already has column | No change needed | ✅ Verified |
| CRUD operations | Already supported | No change needed | ✅ Verified |

## Troubleshooting

### 422 Validation Error on /auth/register

**Error**:
```json
{
  "message": "Error de validación en los datos enviados",
  "status": 422,
  "error": true,
  "data": {
    "errors": [
      {
        "field": "full_name",
        "message": "Field required"
      }
    ]
  }
}
```

**Solution**: Add `full_name` to your register request:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "Your Full Name",     // ← ADD THIS
  "tenant_name": "Company Name"
}
```

### full_name showing as null in responses

**Cause**: If full_name was NULL in database (from old registrations)

**Solution**: Either:
1. Update user manually in database: `UPDATE users SET full_name = 'Name' WHERE id = ?`
2. Ask user to re-register
3. Implement a user profile update endpoint (optional future feature)

## Future Enhancements

Possible future improvements:

1. Allow `full_name` update in user profile endpoint
2. Split `full_name` into `first_name` and `last_name` on display
3. Add name formatting/normalization
4. Add internationalization for name formats
5. Add optional profile picture to User model

## Files Modified

- ✅ `app/api/routers/auth.py` - Updated UserRegister schema and register endpoint
- ✅ `app/services/auth_service.py` - Updated register_owner method signature
- ✅ `test_invitations.py` - Updated test data to include full_name

## Files Verified (No changes needed)

- ✅ `app/models/user.py` - Already has full_name column
- ✅ `app/schemas/user.py` - Already supports full_name
- ✅ `app/services/user_service.py` - Already uses full_name parameter
- ✅ `app/crud/user.py` - Already handles full_name properly

---

**Refactoring Date**: April 4, 2026
**Status**: ✅ Complete and Tested
**All Tests Passing**: ✅ Yes
