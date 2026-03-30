# 🚀 Guía Rápida - Dashboard Persistente

## Flujo de Uso

### 1. **Iniciar Sesión**
```
http://localhost:3000 
  ↓
/login (automático)
  ↓
Ingresa email y contraseña
  ↓
Click "Login"
  ↓
✅ Redirige a /home (DASHBOARD)
```

### 2. **Pantalla Principal**
```
┌──────────────────────────────────────────────┐
│  SIDEBAR (Izquierda)                         │
│  ├─ [Avatar] Tu Nombre                       │
│  ├─ tu@email.com                             │
│  ├─ [Role Badge]                             │
│  │                                           │
│  ├─ Dashboard                                │
│  ├─ My Profile                               │
│  ├─ Settings                                 │
│  ├─ Users (si eres admin)                    │
│  ├─ Restaurants (según rol)                  │
│  ├─ Employees (según rol)                    │
│  ├─ Meals                                    │
│  │                                           │
│  └─ Logout                                   │
│                                              │
│  DASHBOARD (Derecha)                         │
│  ├─ Estadísticas                             │
│  ├─ Actividad Reciente                       │
│  ├─ Tareas Pendientes                        │
│  └─ Características Disponibles               │
└──────────────────────────────────────────────┘
```

---

## 🎯 Navegación

### Opción 1: Click en Opciones del Sidebar
```
Click en "My Profile"
  ↓
La URL cambia: /home → /home/profile
  ↓
El SIDEBAR PERMANECE IGUAL (importante!)
  ↓
Ves tu información de perfil
```

### Opción 2: Volver al Dashboard
```
Click en "Dashboard" en el sidebar
  ↓
La URL cambia: /home/profile → /home
  ↓
Ves el dashboard principal nuevamente
```

### Opción 3: Cambiar Contraseña
```
Click en "Settings"
  ↓
Rellena:
  - Current Password: tu contraseña actual
  - New Password: nueva contraseña (mín 6 caracteres)
  - Confirm Password: repite la nueva
  ↓
Click "Update Password"
  ↓
✅ "Password changed successfully"
```

---

## 🔐 Roles y Permisos

### 📊 ADMIN
**Acceso a todo:**
- Dashboard
- My Profile
- Settings
- **Users Management** ← Solo admins
- Restaurants
- Employees
- Meals

### 🍽️ RESTAURANT_ADMIN
**Puede ver:**
- Dashboard
- My Profile
- Settings
- Restaurants ← Sus restaurantes
- Meals

**NO PUEDE ver:**
- Users Management ❌
- Employees ❌

### 👔 COMPANY_ADMIN
**Puede ver:**
- Dashboard
- My Profile
- Settings
- Employees ← Sus empleados
- Meals

**NO PUEDE ver:**
- Users Management ❌
- Restaurants ❌

### 👨‍💼 EMPLOYEE
**Puede ver:**
- Dashboard
- My Profile
- Settings
- Meals ← Sus meal logs

**NO PUEDE ver:**
- Users Management ❌
- Restaurants ❌
- Employees ❌

---

## 📱 En Mobile

```
┌─────────────────────────┐
│ [☰] Dashboard           │ ← Hamburguesa (abre sidebar)
├─────────────────────────┤
│                         │
│     CONTENIDO PRINCIPAL │
│                         │
│                         │
└─────────────────────────┘

Click en [☰]:
↓
Se abre SIDEBAR deslizable desde la izquierda
↓
Selecciona una opción
↓
El sidebar se cierra automáticamente
```

---

## 🎮 Funciones Especiales

### Dashboard (Estadísticas)
```
Muestra:
- 4 tarjetas con estadísticas principales
- Actividad reciente (últimas 24h)
- Tareas pendientes con progreso
- Características disponibles
```

### My Profile (Ver Información)
```
Muestra:
- Tu nombre completo
- Tu email
- Tu rol actual
- Status (Active)
- Si eres admin: "Administrator Access"
```

### Settings (Cambiar Contraseña)
```
Permite:
- Cambiar tu contraseña
- Futuras opciones de notificaciones
- Futuras opciones de privacidad
```

### Users Management (Admin)
```
Tabla con:
- ID del usuario
- Email
- Nombre completo
- Rol (con color)
- Botón Delete (futuro)

Visible solo para ADMINS
```

---

## ❌ Errores Comunes

### ❌ "You don't have permission to access this page"
```
Significa: Tu rol no tiene acceso a esa página
Solución: Usa tu cuenta con permisos o pide a un admin

Ejemplo:
- Employee intenta acceder a /home/users
- Recibe: "You don't have permission"
- Solución: Necesita ser admin
```

### ❌ "Please login first"
```
Significa: No hay token en localStorage
Solución: 
- Hace logout, haz login de nuevo
- O borra localStorage (F12 → Application → localStorage)
```

### ❌ La sidebar no se ve
```
Means: Estás en mobile/tablet
Solución: Click en el botón [☰] para abrir el drawer

O en desktop: recarga la página (F5)
```

---

## �ています Personalizaciones Futuras

Según tu rol, estas opciones mostrarán contenido diferente:

### Solo para ADMIN
- [ ] Stadísticas de todo el sistema
- [ ] Gráficos avanzados
- [ ] Auditoría de actividades
- [ ] Configuración global

### Solo para RESTAURANT_ADMIN
- [ ] Lista de sus restaurantes
- [ ] Menú de comidas
- [ ] Historial de pedidos

### Solo para COMPANY_ADMIN
- [ ] Lista de empleados
- [ ] Asignación de meal plans
- [ ] Reportes de gasto

### Para EMPLOYEE
- [ ] Mis meal logs
- [ ] Historial de pagos
- [ ] Preferencias de comida

---

## 🚨 La Barra Lateral Permanece (Lo Importante)

**Característica clave:**
```
Mientras navegas entre:
- Dashboard → Profile → Settings → Users → etc

La barra lateral SIEMPRE PERMANECE IGUAL

No se recarga, no se quita, no se mueve

Solo cambias el contenido principal de la derecha
```

---

## ✅ Checklist de Funcionalidad

- [ ] Puedo hacer login
- [ ] Redirige a /home
- [ ] Veo el sidebar en la izquierda (desktop)
- [ ] Veo el dashboard en el centro
- [ ] Mi información se muestra en el sidebar
- [ ] Mi rol aparece con un badge de color
- [ ] Puedo hacer click en "My Profile"
- [ ] La URL cambia pero el sidebar permanece
- [ ] Puedo volver al Dashboard
- [ ] Puedo ir a Settings
- [ ] Puedo cambiar mi contraseña
- [ ] Solo veo opciones según mi rol
- [ ] Puedo hacer click en el icono de Logout
- [ ] Me regresa a /login después del logout

---

## 📞 Troubleshooting

### "El sidebar no aparece"
```bash
# Verifica que estés en desktop (no mobile)
# Intenta: F5 (recargar)
# Abre DevTools: F12 → Check console for errors
```

### "No veo mis opciones"
```bash
# Verifica tu rol en el sidebar
# Si es employee, no verás Users Management
# Eso es correcto ✅
```

### "No puedo cambiar la contraseña"
```bash
# Verifica que la contraseña actual sea correcta
# Verifica que la nueva contraseña sea mín 6 caracteres
# Verifica que ambas nuevas contraseñas coincidan
```

### "Logout no funciona"
```bash
# Intenta: Control+Shift+Delete (limpiar cache)
# O manually delete localStorage (F12 → Application → Storage → Clear)
# Recarga la página
```

---

## 🎓 Conceptos Clave

### 1. **Sidebar Persistente**
- No desaparece cuando cambias de sección
- Siempre está ahí (en desktop)
- Mobile: aparece en drawer

### 2. **Navegación sin Reload**
- Las secciones cambian sin refrescar la página
- Muy rápido y fluido
- El estado se mantiene

### 3. **Control por Rol**
- Cada usuario ve solo lo que puede hacer
- No es posible "forzar" acceso a rutas no permitidas
- Hay validación en 3 niveles

### 4. **Dashboard = Home**
- El dashboard es la página principal
- Todos ven lo mismo (pero con información diferente)
- Desde aquí accedes a todo

---

## 🎉 ¡Listo!

Ahora tienes un **dashboard profesional y moderno** con:
- ✅ Navegación persistente
- ✅ Sidebar dinámico por rol
- ✅ Protección de rutas
- ✅ Responsive design
- ✅ Funcionalidad completa

**¡A disfrutar! 🚀**
