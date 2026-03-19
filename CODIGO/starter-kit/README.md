# MesaPass v2 - Backend

Backend del proyecto MesaPass v2 (FastAPI, SQLAlchemy, PostgreSQL) desplegado en `app/`.

## Estructura del proyecto

```
app/
├── main.py
├── core/
│   ├── config.py
│   ├── security.py
├── db/
│   ├── base.py
│   ├── session.py
├── models/
│   ├── user.py
│   ├── restaurant.py
├── schemas/
│   ├── auth.py
│   ├── restaurant.py
├── routers/
│   ├── auth.py
│   ├── restaurants.py
│   ├── __init__.py
├── services/
│   ├── users.py
│   ├── auth_service.py
│   ├── restaurants.py
├── dependencies/
│   ├── auth.py
├── utils/
```

## Requisitos

- Python 3.12+
- PostgreSQL
- Dependencias Python:
  - fastapi
  - uvicorn
  - sqlalchemy>=2.0
  - asyncpg
  - alembic
  - pydantic>=2.0
  - python-jose
  - passlib[bcrypt]
  - python-dotenv

## Configuración de entorno

Crea el archivo `.env` en la raíz con:

```
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<database>
JWT_SECRET_KEY=super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

##  Ejecutar localmente

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Iniciar servidor:

```bash
uvicorn app.main:app --reload
```

3. Abrir Swagger:

- `http://127.0.0.1:8000/docs`

## Módulo Auth + User + JWT

### Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

### Flujo

1. Registrar y loguear usuario.
2. Recibir token `access` + `refresh`.
3. Usar `Authorization: Bearer <access_token>` en requests protegidos.

## Módulo Restaurants

### Endpoints

- `POST /restaurants`
- `GET /restaurants`
- `GET /restaurants/{id}`
- `PUT /restaurants/{id}`
- `PATCH /restaurants/{id}/deactivate`

### Reglas

- Solo `restaurant_admin` y `super_admin` pueden crear/gestionar.
- RUC único.
- Acceso por propietario (restaurant_admin ve solo los suyos).

##  Arquitectura 3 capas

- `routers` -> rutas API
- `services` -> lógica negocio
- `models` -> SQLAlchemy
- `schemas` -> validación y respuestas Pydantic
- `dependencies` -> control auth/roles

##  Próximos módulos

- Invitation Codes
- Companies
- Agreements
- Employees
- QR Module
- Meal Logs
- Reports

##  Notas

- No modificar la carpeta `src/` (frontend existente).
- Implementar migraciones con Alembic antes de probar.
- Es recomendable agregar tests con `pytest`.

