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

## Orden de ejecución recomendado

1. `Auth -> Register`
   - Registra el tenant y el owner.
   - Guarda `token` y `tenant_id`.

2. `Auth -> Login`
   - Obtiene nuevo token y tenant.
   - Guarda `token` y `tenant_id`.

3. `Auth -> Get Current User`
   - Verifica usuario conectado.
   - Guarda `user_id`.

4. `Users -> Get Users`
   - Lista usuarios del tenant.

5. `Users -> Invite User`
   - Crea una invitación para un nuevo usuario.
   - Guarda `invitation_code`.

6. `Users -> Accept Invitation`
   - Acepta la invitación con `invitation_code`.
   - Guarda `invited_user_id` si está disponible.

7. `Employees -> Create Employee`
   - Crea un empleado para el tenant.
   - Guarda `employee_id` y `qr_token`.

8. `QR -> Get QR Image`
   - Descarga la imagen QR del empleado.

9. `Validación -> Validate QR`
   - Valida el `qr_token` del empleado.

10. `Agreements -> Create Agreement`
    - Crea un convenio para el tenant.
    - Guarda `agreement_id`.

11. `Meal Logs -> Create Meal Log`
    - Registra un consumo usando `employee_id` y `agreement_id`.

12. `Reports -> Consumption Report`
    - Obtiene el reporte de consumo.

13. `Reports -> Billing Report`
    - Obtiene el reporte de facturación.

## Notas importantes

- Todas las requests protegidas deben usar:
  - `Authorization: Bearer {{token}}`
  - `X-Tenant-ID: {{tenant_id}}`

- El backend del proyecto devuelve datos anidados en `data.data`, por lo que los tests de la colección ya usan ese formato.

- Si alguna request falla:
  1. Verifica que el backend esté corriendo.
  2. Confirma que `base_url` apunta a `http://127.0.0.1:8000`.
  3. Revisa el valor de `tenant_id` y `token`.

## Flujo completo de prueba

1. `Register`
2. `Login`
3. `Get Current User`
4. `Get Users`
5. `Invite User`
6. `Accept Invitation`
7. `Create Employee`
8. `Get QR Image`
9. `Validate QR`
10. `Create Agreement`
11. `Create Meal Log`
12. `Consumption Report`
13. `Billing Report`

Así tendrás una prueba completa del proyecto SaaS: registro, autenticación, usuarios, empleados, QR, validación, acuerdos, consumo y facturación.
