# MesaPass Postman Flow

Este README explica el flujo de pruebas para el backend FastAPI SaaS de MesaPass usando la colección `Proyecto_MESAPASS_COMPLETE.json`.

## Requisitos

- Backend ejecutándose en `http://127.0.0.1:8000`
- Postman instalado
- Importar la colección `Proyecto_MESAPASS_COMPLETE.json`

## Variables de entorno

Usa las variables de la colección:

- `base_url` → URL del backend
- `token` → JWT de acceso
- `tenant_id` → ID del tenant seleccionado
- `user_id` → ID del usuario actual
- `employee_id` → ID del empleado creado
- `qr_token` → token QR del empleado
- `agreement_id` → ID del acuerdo creado
- `invitation_code` → código de invitación
- `invited_user_id` → ID del usuario aceptado

## Cambios Recientes (Full Name Support)

**⚠️ IMPORTANTE**: A partir de la refactorización del 4 de abril de 2026:

- El campo `full_name` es ahora **REQUERIDO** en `POST /auth/register`
- El campo `full_name` es ahora **REQUERIDO** en `POST /api/invitations/accept`
- Todos los endpoints de autenticación ahora retornan `full_name` en la respuesta

Ver [FULL_NAME_REFACTOR.md](FULL_NAME_REFACTOR.md) para detalles completos.

## Orden de ejecución recomendado

1. `Auth -> Register`
   - **Registra el tenant y el owner**
   - ⚠️ AHORA REQUIERE `full_name` en el body
   - Guarda `token` y `tenant_id`
   - Ejemplo de body:
   ```json
   {
     "email": "admin@example.com",
     "password": "SecurePass123",
     "full_name": "Juan Pérez",
     "tenant_name": "Mi Empresa"
   }
   ```

2. `Auth -> Login`
   - Obtiene nuevo token y tenant
   - ✅ Retorna `full_name` en la respuesta
   - Guarda `token` y `tenant_id`

3. `Auth -> Get Current User`
   - Verifica usuario conectado
   - ✅ Retorna `full_name` del usuario actual
   - Guarda `user_id`

4. `Users -> Get Users`
   - Lista usuarios del tenant
   - ✅ Cada usuario incluye su `full_name`

5. `Users -> Invite User`
   - Crea una invitación para un nuevo usuario
   - Guarda `invitation_code`

6. `Users -> Accept Invitation`
   - ⚠️ AHORA REQUIERE `full_name` para el usuario invitado
   - Acepta la invitación con `invitation_code`
   - Guarda `invited_user_id` si está disponible
   - Ejemplo de body:
   ```json
   {
     "code": "invitation_code_here",
     "password": "NewPassword123",
     "full_name": "María García"
   }
   ```

7. `Employees -> Create Employee`
   - Crea un empleado para el tenant
   - Guarda `employee_id` y `qr_token`

8. `QR -> Get QR Image`
   - Descarga la imagen QR del empleado

9. `Validación -> Validate QR`
   - Valida el `qr_token` del empleado

10. `Agreements -> Create Agreement`
    - Crea un convenio para el tenant
    - Guarda `agreement_id`

11. `Meal Logs -> Create Meal Log`
    - Registra un consumo usando `employee_id` y `agreement_id`

12. `Reports -> Consumption Report`
    - Obtiene el reporte de consumo

13. `Reports -> Billing Report`
    - Obtiene el reporte de facturación

## Notas importantes

- Todas las requests protegidas deben usar:
  - `Authorization: Bearer {{token}}`
  - `X-Tenant-ID: {{tenant_id}}`

- El backend del proyecto devuelve datos anidados en `data.data`, por lo que los tests de la colección ya usan ese formato

- **Desde abril 2026**: El campo `full_name` debe incluirse en:
  - ✅ `POST /auth/register` (REQUERIDO)
  - ✅ `POST /api/invitations/accept` (REQUERIDO)

- Si alguna request falla:
  1. Verifica que el backend esté corriendo
  2. Confirma que `base_url` apunta a `http://127.0.0.1:8000`
  3. Revisa el valor de `tenant_id` y `token`
  4. Para errores 422 en Register o Accept Invitation: verifica que `full_name` esté incluido en el body

## Flujo completo de prueba

1. `Register` (con full_name)
2. `Login`
3. `Get Current User`
4. `Get Users`
5. `Invite User`
6. `Accept Invitation` (con full_name)
7. `Create Employee`
8. `Get QR Image`
9. `Validate QR`
10. `Create Agreement`
11. `Create Meal Log`
12. `Consumption Report`
13. `Billing Report`

Así tendrás una prueba completa del proyecto SaaS: registro, autenticación, usuarios, empleados, QR, validación, acuerdos, consumo y facturación.

## Testing Full Name Support

Para verificar que el sistema está funcionando correctamente con `full_name`:

```bash
# Ejecutar test de full_name
python test_full_name_registration.py

# O ejecutar el test completo de invitaciones
python test_invitations.py
```

Ambos scripts validan que `full_name` se está almacenando y retornando correctamente.
