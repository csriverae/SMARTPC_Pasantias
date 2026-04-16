# Mobile Device Authentication Guide

## Overview

El sistema de autenticación de dispositivos móviles permite que los usuarios no pasen por el proceso de login nuevamente en sus dispositivos móviles durante 30 días. Una vez que se registra un dispositivo, puede usar `refresh_token` para obtener nuevos `access_token` sin necesidad de ingresar credenciales.

## Architecture

### Database Schema

**Table: `device_sessions`**
- Almacena sesiones de dispositivos activos
- Un dispositivo = una fila en la tabla
- Cada dispositivo tiene un `device_id` único y un `refresh_token` asociado
- Las sesiones expiran después de 30 días

Campos principales:
- `device_id`: Identificador único del dispositivo
- `device_name`: Nombre del dispositivo (ej: "iPhone 12 Pro")
- `device_type`: Tipo de dispositivo (mobile, tablet, web)
- `os`: Sistema operativo (iOS, Android, etc.)
- `refresh_token`: Token de refresco para renovar acceso
- `is_active`: Indica si la sesión está activa
- `expires_at`: Fecha de expiración del token

### Key Components

1. **Model**: `app/models/device_session.py` - Define la estructura de datos
2. **CRUD**: `app/crud/device_session.py` - Operaciones de base de datos
3. **Service**: Methods en `app/services/auth_service.py` - Lógica de negocio
4. **Routers**: `app/api/routers/auth.py` - Endpoints de la API

## API Endpoints

### 1. Mobile Login (Crear Nueva Sesión)

**Endpoint**: `POST /auth/mobile/login`

Autentica al usuario y registra su dispositivo para futuras sesiones automáticas.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "remember_device": true,
  "device_info": {
    "device_id": "unique-device-id",
    "device_name": "iPhone 12 Pro",
    "device_type": "mobile",
    "os": "iOS",
    "os_version": "15.1",
    "app_version": "1.0.0",
    "device_token": "firebase-token-xyz"
  }
}
```

**Response (Success):**
```json
{
  "message": "Mobile login exitoso",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "bearer",
      "device_id": "unique-device-id",
      "tenant_id": "12345",
      "user": {
        "user_id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "tenant_role": "admin",
        "tenants": [...]
      }
    }
  }
}
```

**Headers**: None (para el login)


### 2. Validate Device (Auto-Login)

**Endpoint**: `POST /auth/mobile/validate-device?device_id=unique-device-id`

Valida un dispositivo registrado y devuelve un nuevo `access_token` sin necesidad de login.

**Request**: Solo query parameter

**Response (Success):**
```json
{
  "message": "Dispositivo validado - Login automático",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "is_valid": true,
      "device_id": "unique-device-id",
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "email": "user@example.com"
    }
  }
}
```

**Response (Failed):**
```json
{
  "message": "Dispositivo no válido o sesión expirada",
  "status": 401,
  "error": true,
  "data": {
    "data": {
      "is_valid": false
    }
  }
}
```

**Headers**: None (validate-device es público para permitir auto-login)


### 3. Get User Devices

**Endpoint**: `GET /auth/mobile/devices`

Lista todos los dispositivos registrados del usuario actual.

**Response:**
```json
{
  "message": "Dispositivos obtenidos",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "devices": [
        {
          "device_id": "device-1",
          "device_name": "iPhone 12 Pro",
          "device_type": "mobile",
          "os": "iOS",
          "os_version": "15.1",
          "app_version": "1.0.0",
          "last_accessed": "2026-04-16T10:30:00",
          "created_at": "2026-03-17T10:30:00"
        },
        {
          "device_id": "device-2",
          "device_name": "Samsung Galaxy S21",
          "device_type": "mobile",
          "os": "Android",
          "os_version": "12.0",
          "app_version": "1.0.0",
          "last_accessed": "2026-04-15T14:20:00",
          "created_at": "2026-04-01T14:20:00"
        }
      ],
      "total": 2
    }
  }
}
```

**Headers**: 
```
Authorization: Bearer <access_token>
```


### 4. Update Device Token (Push Notifications)

**Endpoint**: `POST /auth/mobile/update-device-token?device_id=unique-device-id&device_token=firebase-token`

Actualiza el token de Firebase para notificaciones push.

**Response:**
```json
{
  "message": "Token de dispositivo actualizado",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "device_id": "unique-device-id",
      "device_token": "firebase-token-xyz"
    }
  }
}
```

**Headers**: 
```
Authorization: Bearer <access_token>
```


### 5. Logout from Device

**Endpoint**: `POST /auth/mobile/logout-device?device_id=unique-device-id`

Cierra sesión en un dispositivo específico.

**Response:**
```json
{
  "message": "Sesión cerrada en el dispositivo",
  "status": 200,
  "error": false,
  "data": {
    "data": null
  }
}
```

**Headers**: 
```
Authorization: Bearer <access_token>
```


### 6. Logout from All Devices

**Endpoint**: `POST /auth/mobile/logout-all-devices`

Cierra sesión en todos los dispositivos (recomendado después de cambiar contraseña).

**Response:**
```json
{
  "message": "Sesión cerrada en todos los dispositivos (3 dispositivos)",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "devices_logged_out": 3
    }
  }
}
```

**Headers**: 
```
Authorization: Bearer <access_token>
```


## Client Implementation Guide

### React Native / Flutter / Native Mobile App

#### 1. First Login (User enters credentials)

```typescript
// 1. Login with credentials and device info
const response = await fetch('/auth/mobile/login', {
  method: 'POST',
  body: JSON.stringify({
    email: userEmail,
    password: userPassword,
    remember_device: true,
    device_info: {
      device_id: getUniqueDeviceId(),  // Use native API
      device_name: getDeviceName(),
      device_type: 'mobile',
      os: getOS(),
      os_version: getOSVersion(),
      app_version: APP_VERSION,
      device_token: fcmToken
    }
  })
});

const loginData = await response.json();

// 2. Save tokens securely
await SecureStorage.setItem('access_token', loginData.data.data.access_token);
await SecureStorage.setItem('refresh_token', loginData.data.data.refresh_token);
await SecureStorage.setItem('device_id', loginData.data.data.device_id);
```

#### 2. App Startup (Auto-Login)

```typescript
// 1. Check if device is registered
const deviceId = await SecureStorage.getItem('device_id');
if (deviceId) {
  // 2. Validate device and get new access token
  const response = await fetch(`/auth/mobile/validate-device?device_id=${deviceId}`);
  const validation = await response.json();
  
  if (validation.data.data.is_valid) {
    // 3. Use new access token
    await SecureStorage.setItem('access_token', validation.data.data.access_token);
    // Auto-login successful, navigate to main screen
  } else {
    // Device session expired, go to login
  }
} else {
  // First time, go to login
}
```

#### 3. Token Refresh (When access token expires)

```typescript
// Using existing refresh token mechanism
const response = await fetch('/auth/refresh-token', {
  method: 'POST',
  body: JSON.stringify({
    refresh_token: await SecureStorage.getItem('refresh_token')
  })
});

const newTokens = await response.json();
await SecureStorage.setItem('access_token', newTokens.data.data.access_token);

// Device session is also updated automatically
```

#### 4. Manage Devices (Show all logged-in devices)

```typescript
// Get all devices
const response = await fetch('/auth/mobile/devices', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const { data } = await response.json();
// Display list of devices to user
displayDevicesList(data.data.devices);
```

#### 5. Logout from Specific Device

```typescript
const response = await fetch(
  `/auth/mobile/logout-device?device_id=${deviceId}`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }
);

// Device session is now inactive
```

#### 6. Logout from All Devices (Security measure)

```typescript
// When changing password
const response = await fetch('/auth/mobile/logout-all-devices', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// All device sessions are now inactive
// User needs to login again on all devices
```


## Security Considerations

1. **Device ID Generation**: Usar identificadores únicos nativos del dispositivo:
   - iOS: `UIDevice.current.identifierForVendor`
   - Android: `android.os.Build.ID` o Firebase Instance ID

2. **Secure Token Storage**: 
   - Usar Keychain (iOS) o Keystore (Android)
   - NUNCA guardar tokens en SharedPreferences o UserDefaults

3. **Token Expiration**: 
   - Access token: 15 minutos (estándar)
   - Device session: 30 días (configurable)
   - Refresh token: 30 días

4. **Logout on Password Change**: 
   - Implementar logout de todos los dispositivos
   - Fuerza re-autenticación en la próxima solicitud

5. **Firebase Token Update**: 
   - Actualizar el `device_token` cuando cambia
   - Permite enviar notificaciones push al dispositivo

6. **Session Invalidation**: 
   - Deactivate device si hay sospecha de hack
   - Mostrar lista de dispositivos activos para auditoría


## Database Maintenance

### Cleanup Expired Sessions

```python
# Ejecutar periódicamente (por ejemplo, con Celery)
from app.crud.device_session import cleanup_expired_sessions

expired_count = cleanup_expired_sessions(db)
print(f"Cleaned up {expired_count} expired sessions")
```

### Monitor Device Sessions

```sql
-- Ver dispositivos activos por usuario
SELECT * FROM device_sessions 
WHERE user_id = 1 AND is_active = TRUE 
ORDER BY last_accessed DESC;

-- Ver todos los dispositivos registrados
SELECT COUNT(*) as total_devices FROM device_sessions;

-- Ver dispositivos que expiran pronto
SELECT * FROM device_sessions 
WHERE expires_at < NOW() + INTERVAL 7 DAY AND is_active = TRUE;
```


## Error Handling

| Error | Status | Meaning | Action |
|-------|--------|---------|--------|
| "Dispositivo no válido o sesión expirada" | 401 | Device session expired | Go to login screen |
| "Usuario no encontrado" | 401 | User doesn't exist | Go to login screen |
| "No tienes permiso para actualizar este dispositivo" | 403 | Trying to update another user's device | Show error message |
| "Error validando dispositivo" | 500 | Server error | Retry or go to login |


## Configuration

En `app/core/config.py` (si es necesario personalizar):

```python
# Device session expiration
DEVICE_SESSION_EXPIRE_DAYS = 30  # days
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # minutes
REFRESH_TOKEN_EXPIRE_DAYS = 30  # days
```


## Future Enhancements

1. **Device Fingerprinting**: Adicionar validación de características del dispositivo
2. **Biometric Authentication**: Integrar Face ID / Touch ID
3. **Device Management UI**: Interfaz para gestionar dispositivos en el dashboard
4. **Location-based Challenge**: Requerir verificación si el dispositivo cambia de ubicación significativamente
5. **Activity Logs**: Registrar logins y accesos por dispositivo
6. **Rate Limiting**: Limitar intentos de auto-login fallidos
