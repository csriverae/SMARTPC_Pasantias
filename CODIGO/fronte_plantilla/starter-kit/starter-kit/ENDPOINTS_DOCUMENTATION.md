# MesaPass v2 Backend - Documentación de Endpoints

## AUTH

### Endpoint: POST /auth/register
**Descripción:** Registrar nuevo usuario

**Campos obligatorios:** name, email, password

Body:
```json
{
  "name": "Juan Pérez",
  "email": "juan.perez@example.com",
  "password": "SecurePass123!"
}
```

---

### Endpoint: POST /auth/login
**Descripción:** Iniciar sesión y obtener token JWT

**Campos obligatorios:** email, password

Body:
```json
{
  "email": "juan.perez@example.com",
  "password": "SecurePass123!"
}
```

Response:
```json
{
  "message": "Login exitoso",
  "status": 200,
  "error": false,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Juan Pérez",
      "email": "juan.perez@example.com",
      "role": "employee"
    }
  }
}
```

---

### Endpoint: GET /auth/me
**Descripción:** Obtener información del usuario autenticado

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Usuario actual",
  "status": 200,
  "error": false,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "juan.perez@example.com",
    "name": "Juan Pérez",
    "role": "employee"
  }
}
```

---

## USERS

### Endpoint: GET /users
**Descripción:** Listar todos los usuarios

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Usuarios obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "users": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "role": "employee"
      },
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "name": "María García",
        "email": "maria.garcia@example.com",
        "role": "admin"
      }
    ]
  }
}
```

---

### Endpoint: GET /users/{user_id}
**Descripción:** Obtener datos de un usuario específico

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Usuario encontrado",
  "status": 200,
  "error": false,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Juan Pérez",
      "email": "juan.perez@example.com",
      "role": "employee"
    }
  }
}
```

---

### Endpoint: PUT /users/{user_id}
**Descripción:** Actualizar datos de un usuario

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos opcionales:** name, email, role

Body:
```json
{
  "name": "Juan Pérez Actualizado",
  "role": "restaurant_admin"
}
```

---

### Endpoint: DELETE /users/{user_id}
**Descripción:** Eliminar un usuario

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

---

## RESTAURANTS

### Endpoint: POST /restaurants
**Descripción:** Crear nuevo restaurante

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos obligatorios:** name, owner_id

Body:
```json
{
  "name": "La Cocina Bogotá",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### Endpoint: GET /restaurants
**Descripción:** Listar todos los restaurantes

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Restaurantes obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "restaurants": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "name": "La Cocina Bogotá",
        "owner_id": "550e8400-e29b-41d4-a716-446655440000"
      },
      {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "name": "El Sabor Caleño",
        "owner_id": "660e8400-e29b-41d4-a716-446655440001"
      }
    ]
  }
}
```

---

### Endpoint: GET /restaurants/{restaurant_id}
**Descripción:** Obtener datos de un restaurante específico

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Restaurante encontrado",
  "status": 200,
  "error": false,
  "data": {
    "restaurant": {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "name": "La Cocina Bogotá",
      "owner_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

---

### Endpoint: PUT /restaurants/{restaurant_id}
**Descripción:** Actualizar datos de un restaurante

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos opcionales:** name, owner_id

Body:
```json
{
  "name": "La Cocina Bogotá Premium"
}
```

---

### Endpoint: DELETE /restaurants/{restaurant_id}
**Descripción:** Eliminar un restaurante

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

---

## COMPANIES

### Endpoint: POST /companies
**Descripción:** Crear nueva compañía

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos obligatorios:** name, owner_id

Body:
```json
{
  "name": "TechCorp SAS",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### Endpoint: GET /companies
**Descripción:** Listar todas las compañías

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Compañías obtenidas",
  "status": 200,
  "error": false,
  "data": {
    "companies": [
      {
        "id": "990e8400-e29b-41d4-a716-446655440004",
        "name": "TechCorp SAS",
        "owner_id": "550e8400-e29b-41d4-a716-446655440000"
      },
      {
        "id": "aa0e8400-e29b-41d4-a716-446655440005",
        "name": "Innovatech Ltd",
        "owner_id": "660e8400-e29b-41d4-a716-446655440001"
      }
    ]
  }
}
```

---

### Endpoint: GET /companies/{company_id}
**Descripción:** Obtener datos de una compañía específica

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Compañía encontrada",
  "status": 200,
  "error": false,
  "data": {
    "company": {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "name": "TechCorp SAS",
      "owner_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

---

### Endpoint: PUT /companies/{company_id}
**Descripción:** Actualizar datos de una compañía

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos opcionales:** name, owner_id

Body:
```json
{
  "name": "TechCorp Global SAS"
}
```

---

### Endpoint: DELETE /companies/{company_id}
**Descripción:** Eliminar una compañía

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

---

## EMPLOYEES

### Endpoint: POST /employees
**Descripción:** Crear nuevo empleado

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos obligatorios:** user_id, restaurant_id, company_id

Body:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
  "company_id": "990e8400-e29b-41d4-a716-446655440004"
}
```

---

### Endpoint: GET /employees
**Descripción:** Listar todos los empleados

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Empleados obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "employees": [
      {
        "id": "bb0e8400-e29b-41d4-a716-446655440006",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
        "company_id": "990e8400-e29b-41d4-a716-446655440004"
      }
    ]
  }
}
```

---

### Endpoint: GET /employees/{employee_id}
**Descripción:** Obtener datos de un empleado específico

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Empleado encontrado",
  "status": 200,
  "error": false,
  "data": {
    "employee": {
      "id": "bb0e8400-e29b-41d4-a716-446655440006",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
      "company_id": "990e8400-e29b-41d4-a716-446655440004"
    }
  }
}
```

---

### Endpoint: PUT /employees/{employee_id}
**Descripción:** Actualizar datos de un empleado

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos opcionales:** user_id, restaurant_id, company_id

Body:
```json
{
  "restaurant_id": "880e8400-e29b-41d4-a716-446655440003"
}
```

---

### Endpoint: DELETE /employees/{employee_id}
**Descripción:** Eliminar un empleado

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

---

## AGREEMENTS

### Endpoint: POST /agreements
**Descripción:** Crear nuevo acuerdo entre compañía y restaurante

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos obligatorios:** company_id, restaurant_id, terms, signed_at

Body:
```json
{
  "company_id": "990e8400-e29b-41d4-a716-446655440004",
  "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
  "terms": "Acuerdo de comidas subsidiadas para empleados - 1 comida gratis por día laboral",
  "signed_at": "2026-03-27T10:30:00Z"
}
```

---

### Endpoint: GET /agreements
**Descripción:** Listar todos los acuerdos

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Acuerdos obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "agreements": [
      {
        "id": "cc0e8400-e29b-41d4-a716-446655440007",
        "company_id": "990e8400-e29b-41d4-a716-446655440004",
        "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
        "terms": "Acuerdo de comidas subsidiadas para empleados - 1 comida gratis por día laboral",
        "signed_at": "2026-03-27T10:30:00Z"
      }
    ]
  }
}
```

---

### Endpoint: GET /agreements/{agreement_id}
**Descripción:** Obtener datos de un acuerdo específico

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Acuerdo encontrado",
  "status": 200,
  "error": false,
  "data": {
    "agreement": {
      "id": "cc0e8400-e29b-41d4-a716-446655440007",
      "company_id": "990e8400-e29b-41d4-a716-446655440004",
      "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
      "terms": "Acuerdo de comidas subsidiadas para empleados - 1 comida gratis por día laboral",
      "signed_at": "2026-03-27T10:30:00Z"
    }
  }
}
```

---

### Endpoint: PUT /agreements/{agreement_id}
**Descripción:** Actualizar un acuerdo

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos opcionales:** company_id, restaurant_id, terms, signed_at

Body:
```json
{
  "terms": "Acuerdo actualizado: 2 comidas gratis por día laboral"
}
```

---

### Endpoint: DELETE /agreements/{agreement_id}
**Descripción:** Eliminar un acuerdo

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

---

## INVITATION CODES

### Endpoint: POST /invitation-codes
**Descripción:** Crear código de invitación

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos obligatorios:** code

**Campos opcionales:** is_used (default: false)

Body:
```json
{
  "code": "MESAS2026TECH001",
  "is_used": false
}
```

---

### Endpoint: GET /invitation-codes
**Descripción:** Listar todos los códigos de invitación

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Códigos de invitación obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "invitation_codes": [
      {
        "id": "dd0e8400-e29b-41d4-a716-446655440008",
        "code": "MESAS2026TECH001",
        "is_used": false
      },
      {
        "id": "ee0e8400-e29b-41d4-a716-446655440009",
        "code": "MESAS2026CORP002",
        "is_used": true
      }
    ]
  }
}
```

---

### Endpoint: GET /invitation-codes/{code_id}
**Descripción:** Obtener un código de invitación específico

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Código de invitación encontrado",
  "status": 200,
  "error": false,
  "data": {
    "invitation_code": {
      "id": "dd0e8400-e29b-41d4-a716-446655440008",
      "code": "MESAS2026TECH001",
      "is_used": false
    }
  }
}
```

---

### Endpoint: PUT /invitation-codes/{code_id}
**Descripción:** Actualizar un código de invitación

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

**Campos opcionales:** code, is_used

Body:
```json
{
  "is_used": true
}
```

---

### Endpoint: DELETE /invitation-codes/{code_id}
**Descripción:** Eliminar un código de invitación

**Headers requeridos:** Authorization: Bearer {token}

**Role requerido:** admin

---

## MEAL LOGS

### Endpoint: POST /meal-logs
**Descripción:** Registrar consumo de comida

**Headers requeridos:** Authorization: Bearer {token}

**Campos obligatorios:** user_id, restaurant_id, meal_type, consumed_at

Body:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
  "meal_type": "lunch",
  "consumed_at": "2026-03-27T12:30:00Z"
}
```

---

### Endpoint: GET /meal-logs
**Descripción:** Listar todos los registros de comidas

**Headers requeridos:** Authorization: Bearer {token}

Query parameters (opcionales):
- skip: número de registros a saltar (default: 0)
- limit: cantidad de registros (default: 100)

Response:
```json
{
  "message": "Registros de comidas obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "meal_logs": [
      {
        "id": "ff0e8400-e29b-41d4-a716-446655440010",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
        "meal_type": "lunch",
        "consumed_at": "2026-03-27T12:30:00Z"
      },
      {
        "id": "gg0e8400-e29b-41d4-a716-446655440011",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
        "meal_type": "breakfast",
        "consumed_at": "2026-03-27T08:00:00Z"
      }
    ]
  }
}
```

---

### Endpoint: GET /meal-logs/{meal_log_id}
**Descripción:** Obtener un registro de comida específico

**Headers requeridos:** Authorization: Bearer {token}

Response:
```json
{
  "message": "Registro de comida encontrado",
  "status": 200,
  "error": false,
  "data": {
    "meal_log": {
      "id": "ff0e8400-e29b-41d4-a716-446655440010",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "restaurant_id": "770e8400-e29b-41d4-a716-446655440002",
      "meal_type": "lunch",
      "consumed_at": "2026-03-27T12:30:00Z"
    }
  }
}
```

---

### Endpoint: PUT /meal-logs/{meal_log_id}
**Descripción:** Actualizar un registro de comida

**Headers requeridos:** Authorization: Bearer {token}

**Campos opcionales:** user_id, restaurant_id, meal_type, consumed_at

Body:
```json
{
  "meal_type": "dinner",
  "consumed_at": "2026-03-27T19:00:00Z"
}
```

---

### Endpoint: DELETE /meal-logs/{meal_log_id}
**Descripción:** Eliminar un registro de comida

**Headers requeridos:** Authorization: Bearer {token}

---

## CÓDIGOS DE ERROR

### Error 400 - Bad Request
```json
{
  "message": "Email y contraseña requeridos",
  "status": 400,
  "error": true,
  "data": {
    "data": []
  }
}
```

### Error 401 - Unauthorized (Token inválido)
```json
{
  "message": "Token inválido",
  "status": 401,
  "error": true,
  "data": {
    "data": [],
    "error": "Token inválido o expirado"
  }
}
```

### Error 403 - Forbidden (Permiso insuficiente)
```json
{
  "message": "Role no autorizado",
  "status": 403,
  "error": true,
  "data": {
    "data": []
  }
}
```

### Error 404 - Not Found
```json
{
  "message": "Usuario no encontrado",
  "status": 404,
  "error": true,
  "data": {
    "data": []
  }
}
```

### Error 500 - Server Error
```json
{
  "message": "Error interno en el servidor",
  "status": 500,
  "error": true,
  "data": {
    "data": [],
    "error": "mensaje de error específico"
  }
}
```

---

## CONFIGURACIÓN DE BASE DE DATOS

**Base de datos:** PostgreSQL
**Host:** localhost
**Puerto:** 54345
**Database:** mesa_db
**Usuario:** postgres
**Contraseña:** 1234

---

## CONFIGURACIÓN DE ENTORNO

**Base URL:** http://127.0.0.1:8000
**Content-Type:** application/json
**Authorization Header:** Bearer {token}

---

## TIPOS DE ROLES

- **admin:** Acceso total a todos los endpoints
- **restaurant_admin:** Acceso a gestión de su restaurante
- **company_admin:** Acceso a gestión de su compañía
- **employee:** Acceso limitado, solo lectura de información de acuerdos y restaurantes

