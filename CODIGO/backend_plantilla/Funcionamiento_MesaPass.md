# Funcionamiento_MesaPass

## Resumen general
MesaPass es un backend de FastAPI con arquitectura SaaS multi-tenant. El núcleo se encuentra en `starter-kit/starter-kit/app`, usando SQLAlchemy para la base de datos y JWT para autenticación.

El servidor principal se inicia con `starter-kit/starter-kit/run_server.py` y expone rutas en `app/main.py`. La base de datos se crea automáticamente en el arranque mediante `Base.metadata.create_all(bind=engine)`.

---

## Archivos importantes

### Entrada y configuración
- `starter-kit/starter-kit/app/main.py`
  - `FastAPI` app
  - middleware CORS para `http://localhost:3000`
  - routers principales: `auth`, `employees`, `users`, `invitations`, `agreements`, `meal_logs`, `qr`, `reports`, `companies`, `restaurants`.
  - endpoints de salud: `/` y `/health`.

- `starter-kit/starter-kit/app/core/config.py`
  - `Settings` con variables de entorno:
    - `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
    - `SECRET_KEY`, `ALGORITHM`
    - `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
  - propiedad `DATABASE_URL` usada por SQLAlchemy.

- `starter-kit/starter-kit/app/core/security.py`
  - `get_password_hash`, `verify_password`
  - `create_access_token`, `create_refresh_token`, `verify_token`
  - `get_current_user` que valida JWT Bearer y devuelve el usuario
  - `require_roles` para control de acceso por rol
  - `get_current_tenant` para validar `X-Tenant-ID`
  - `generate_unique_token` para QR codes.

### Base de datos
- `starter-kit/starter-kit/app/db/session.py`
  - `engine` crea la conexión con `DATABASE_URL`
  - `SessionLocal` es la sesión SQLAlchemy.

- `starter-kit/starter-kit/app/db/base.py`
  - `Base = declarative_base()`.

### Modelos clave
- `starter-kit/starter-kit/app/models/user.py`
  - `User` con campos: `email`, `password`, `full_name`, `phone`, `address`, `role`
  - enum `UserRole`: `admin`, `restaurant_admin`, `company_admin`, `employee`.

- `starter-kit/starter-kit/app/models/tenant.py`
  - tenant multi-tenant.

- `starter-kit/starter-kit/app/models/user_tenant.py`
  - relación usuario-tenant con rol dentro del tenant.

- `starter-kit/starter-kit/app/models/company.py`
  - empresas que contratan acuerdos.

- `starter-kit/starter-kit/app/models/restaurant.py`
  - restaurantes del tenant.

- `starter-kit/starter-kit/app/models/agreement.py`
  - acuerdos entre `company` y `restaurant` con fechas `start_date` y `end_date`.

- `starter-kit/starter-kit/app/models/employee.py`
  - empleados con `qr_token`, `company_id`, `company_tenant_id`.

- `starter-kit/starter-kit/app/models/meal_log.py`
  - registros de consumo con `employee_id`, `agreement_id`, `date`, `meal_type`, `total_amount`, `tenant_id`.

- `starter-kit/starter-kit/app/models/user_invitation.py`
  - invitaciones de usuario con estado, código, expiración.

---

## Lógica de negocio y servicios

### Autenticación
- `starter-kit/starter-kit/app/services/auth_service.py`
  - `authenticate_user(db, email, password)`
  - `get_user_tenants(db, user_id)`
  - `create_tokens(user_id, tenant_id, email, role)`
  - `register_owner(db, email, password, full_name, tenant_name, phone, address)`
  - `delete_user(db, user_id, current_user_id, tenant_id)`
  - métodos para registro y validación de sesiones de dispositivo.

### Usuarios
- `starter-kit/starter-kit/app/services/user_service.py`
  - `create_user(...)` crea usuario y lo asigna a un tenant.
  - `get_tenant_users(db, tenant_id)` devuelve usuarios de un tenant.
  - `update_user_role(db, user_id, tenant_id, new_role)` cambia rol dentro del tenant.
  - `delete_tenant_user(db, user_id, tenant_id)` elimina relación usuario-tenant.

### Invitaciones
- `starter-kit/starter-kit/app/services/invitation_service.py`
  - `create_invitation(db, email, tenant_id, invited_by, role, expires_days)`
  - `accept_invitation(db, code, full_name, password)`
  - `get_tenant_invitations(db, tenant_id)`
  - `cancel_invitation(db, invitation_id, tenant_id)`
  - genera códigos y contraseñas temporales.

### Código QR
- `starter-kit/starter-kit/app/services/qr_service.py`
  - `generate_qr_image(employee_id, qr_token)`
  - `get_employee_qr_image(db, employee_id, tenant_id)`
  - `get_qr_code_base64(employee_id, qr_token)`
  - `validate_qr_token(db, qr_token, tenant_id)`

### Reportes
- `starter-kit/starter-kit/app/services/report_service.py`
  - `get_consumption_report(...)` agrega consumo por empleado, tipo de comida y día.
  - `get_billing_report(...)` agrupa por acuerdo y calcula facturación.

---

## Endpoints principales

### Auth
- `POST /auth/register`
  - Registra un tenant y usuario owner.
  - Body: `email`, `password`, `full_name`, `tenant_name`, `phone?`, `address?`.

- `POST /auth/login`
  - Login y devuelve `access_token`, `refresh_token`, `tenant_id`, datos de usuario.
  - Body: `email`, `password`.

- `POST /auth/refresh-token`
  - Refresca token de acceso usando refresh token.

- `POST /auth/password-reset/request`
  - Solicita reset de contraseña.

- `POST /auth/password-reset/confirm`
  - Confirma código de reset y actualiza contraseña.

### Users
- `GET /api/users`
  - Obtiene usuarios de un tenant.
  - Headers: `Authorization: Bearer <token>`, `X-Tenant-ID: <tenant_id>`.

- `POST /api/users/invite`
  - Crea invitación para email.
  - Body: `email`, `role`.

- `PATCH /api/users/{user_id}/role`
  - Actualiza rol de usuario.

- `DELETE /api/users/{user_id}`
  - Elimina usuario del tenant.

### Invitations
- `POST /api/invitations`
  - Crea invitación de usuario.
  - Body: `email`, `expires_days`.

- `POST /api/invitations/accept`
  - Acepta invitación pública.
  - Body: `code`, `full_name`, `password?`.

### Agreements
- `POST /api/agreements`
  - Crea acuerdo `company_id`, `restaurant_id`, `start_date`, `end_date`.

- `GET /api/agreements`
  - Lista acuerdos del tenant.
  - Query opcional `company_id`.

### Meal logs
- `POST /api/meal-logs`
  - Registra consumo de un empleado.
  - Body: `employee_id`, `agreement_id`, `meal_type`, `total_amount`.

- `GET /api/meal-logs`
  - Lista consumos.
  - Query opcional: `employee_id`, `start_date`, `end_date`.

- `GET /api/meal-logs/employee/{employee_id}/consumption`
  - Reporte de consumo por empleado.

### QR
- `GET /api/employees/{employee_id}/qr`
  - Devuelve imagen PNG del QR de empleado.

- `POST /api/validate-qr`
  - Valida token QR.
  - Body: `qr_token`.

- `GET /api/generate-qr-code/{employee_id}`
  - Genera QR en base64 y texto.

### Reports
- `GET /api/reports/consumption`
  - Reporte de consumo por fecha y empleado.
  - Query opcional: `start_date`, `end_date`, `employee_id`.

- `GET /api/reports/billing`
  - Reporte de facturación por acuerdo.
  - Query opcional: `start_date`, `end_date`.

### Companies
- `POST /api/companies`
  - Crea compañía.
  - Body: `name`, `ruc`.

- `GET /api/companies`
  - Lista compañías del tenant.

- `GET /api/companies/{company_id}`
  - Obtiene compañía por ID.

### Restaurants
- `POST /api/restaurants`
  - Crea restaurante.
  - Body: `name`.

- `GET /api/restaurants`
  - Lista restaurantes del tenant.

- `GET /api/restaurants/{restaurant_id}`
  - Obtiene restaurante por ID.

---

## Variables importantes

- `SECRET_KEY`: clave para JWT.
- `ALGORITHM`: `HS256`.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: duración de acceso.
- `REFRESH_TOKEN_EXPIRE_DAYS`: duración de refresh token.
- `DATABASE_URL`: `postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}`.
- Cabeceras requeridas para rutas protegidas:
  - `Authorization: Bearer <access_token>`
  - `X-Tenant-ID: <tenant_id>`

---

## Cómo correr el proyecto

1. Activar virtual environment.
2. Revisar `starter-kit/starter-kit/app/core/config.py` y `.env` si existe.
3. Ejecutar `starter-kit/starter-kit/run_server.py`.
4. Abrir `http://127.0.0.1:8000/docs` para ver documentación Swagger.

---

## Notas adicionales

- El proyecto mezcla soporte multi-tenant con compatibilidad legacy.
- Los routers usan respuestas JSON con estructura estándar: `message`, `status`, `error`, `data`.
- El flujo principal es:
  1. Crear tenant y owner por `/auth/register`.
  2. Loguear con `/auth/login`.
  3. Crear compañías y restaurantes.
  4. Crear acuerdos entre compañías y restaurantes.
  5. Invitar usuarios y registrar consumos.
  6. Generar reportes y validar QR.

- Hay otros ficheros útiles en la raíz como `FLUJO_MESAPASS.md`, `TECHNICAL_GUIDE.md`, `README.md` y `README_TESTS.md`.
