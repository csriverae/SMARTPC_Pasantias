# Configuración Postman para MesaPass SaaS - Flujo Completo

## Base de Datos Configurada ✅
- **Host**: localhost
- **Puerto**: 5434
- **Base de Datos**: mesa_db
- **Usuario**: postgres
- **Contraseña**: 1324

## Pasos para Usar la Colección Postman

### 1️⃣ Importar la Colección
1. Abre Postman
2. Click en `Import`
3. Selecciona el archivo `Proyecto_MESAPASS_COMPLETE.json`
4. Haz click en `Import`

### 2️⃣ Configurar Variables de Entorno
En Postman, configura estas variables:
- `base_url`: `http://127.0.0.1:8000`
- `token`: (se configura automáticamente)
- `tenant_id`: (se configura automáticamente)
- `company_id`: (se configura automáticamente)
- `restaurant_id`: (se configura automáticamente)
- `employee_id`: (se configura automáticamente)
- `agreement_id`: (se configura automáticamente)

### 3️⃣ Asegurate que el Backend esté Corriendo
```bash
# En la carpeta starter-kit/starter-kit
python run_server.py
```

### 4️⃣ Flujo Completo de Pruebas - Orden Recomendado

#### **A. Autenticación**
1. **Login** → Obtiene token y tenant_id automáticamente
2. **Get Current User** → Verifica autenticación

#### **B. Crear Entidades Base**
1. **Create Company** → Crea una compañía (guarda company_id)
2. **Create Restaurant** → Crea un restaurante (guarda restaurant_id)

#### **C. Crear Acuerdos**
1. **Create Agreement** → Crea acuerdo entre compañía y restaurante (guarda agreement_id)

#### **D. Gestionar Empleados**
1. **Create Employee** → Crea empleado en la compañía (guarda employee_id y qr_token)
2. **Get Employees** → Lista empleados
3. **Get Employee QR** → Obtiene código QR del empleado

#### **E. Validación QR**
1. **Validate QR** → Valida token QR del empleado

#### **F. Registros de Comidas**
1. **Create Meal Log** → Registra consumo de comida
2. **Get Meal Logs** → Lista registros de comidas

#### **G. Reportes**
1. **Consumption Report** → Reporte de consumo por empleado
2. **Billing Report** → Reporte de facturación

### 5️⃣ Variables Automáticas
Después de cada request exitoso, estas variables se guardan automáticamente:
- `token` - Token de acceso JWT
- `tenant_id` - ID del tenant actual
- `company_id` - ID de la compañía creada
- `restaurant_id` - ID del restaurante creado
- `employee_id` - ID del empleado creado
- `qr_token` - Token QR del empleado
- `agreement_id` - ID del acuerdo creado

### 6️⃣ Endpoints Disponibles por Categoría

#### 🔐 **Auth**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/me` | Obtener usuario actual |

#### 🏢 **Entities**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/companies` | Crear compañía |
| GET | `/api/companies` | Listar compañías |
| POST | `/api/restaurants` | Crear restaurante |
| GET | `/api/restaurants` | Listar restaurantes |

#### 🤝 **Agreements**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/agreements` | Crear acuerdo |
| GET | `/api/agreements` | Listar acuerdos |

#### 👥 **Employees**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/employees` | Crear empleado |
| GET | `/api/employees` | Listar empleados |
| GET | `/api/employees/{id}/qr` | Obtener QR de empleado |

#### 📱 **QR**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/validate` | Validar token QR |

#### 🍽️ **Meal Logs**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/meal-logs` | Crear registro de comida |
| GET | `/api/meal-logs` | Listar registros |

#### 📊 **Reports**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/reports/consumption` | Reporte de consumo |
| GET | `/api/reports/billing` | Reporte de facturación |

## 🔍 Verificar en PostgreSQL

Para ver que los datos se guardaron en la BD:

```bash
# Conectarte a la BD
psql -h localhost -p 5434 -U postgres -d mesa_db

# Verificar datos creados:
SELECT id, name FROM companies;
SELECT id, name FROM restaurants;
SELECT id, company_id, restaurant_id FROM agreements;
SELECT id, name, email FROM employees;
SELECT id, employee_id, meal_type FROM meal_logs;
```

## 📌 Notas Importantes

1. ⚠️ Todos los endpoints requieren header `X-Tenant-ID` para multi-tenancy
2. ⚠️ Las entidades deben crearse en orden: Company → Restaurant → Agreement → Employee
3. ✅ Los IDs se guardan automáticamente en variables de Postman
4. ✅ El sistema es multi-tenant: cada usuario pertenece a un tenant específico
5. ✅ Los tokens JWT expiran después de 30 minutos

## 🆘 Troubleshooting

### Error: "Connection refused"
```
❌ El backend no está corriendo
✅ Ejecuta: python run_server.py
```

### Error: Foreign key violation
```
❌ Entidades padre no existen (company_id, restaurant_id)
✅ Sigue el orden: Company → Restaurant → Agreement → Employee
```

### Error: "User does not belong to tenant"
```
❌ Token no incluye tenant válido
✅ Asegurate de hacer Login primero para obtener tenant_id
```

### Error: "Field required"
```
❌ Faltan campos requeridos en el body
✅ Revisa la documentación del schema en cada endpoint
```
```
❌ El email ya existe en la base de datos
✅ Usa un email diferente o elimina el usuario de la BD
```

### Error: "Incorrect email or password"
```
❌ Las credenciales son incorrectas
✅ Verifica que escribiste correctamente el email y contraseña
```

### Error: "Invalid token" en otros endpoints
```
❌ El token expiró o no es válido
✅ Haz login nuevamente para obtener un nuevo token
```
