import requests

BASE_URL = "http://127.0.0.1:8000/auth"

# 1) Registrar admin y employee (role explicito)
for user in [
    {"email": "admin@example.com", "password": "admin123", "full_name": "Admin Test", "role": "admin"},
    {"email": "employee@example.com", "password": "employee123", "full_name": "Employee Test", "role": "employee"},
]:
    r = requests.post(f"{BASE_URL}/register", json=user)
    print("register", user['email'], r.status_code, r.text)

# 2) Login admin y employee
tokens = {}
for user in [
    {"email": "admin@example.com", "password": "admin123"},
    {"email": "employee@example.com", "password": "employee123"},
]:
    r = requests.post(f"{BASE_URL}/login", json=user)
    print("login", user['email'], r.status_code, r.text)
    if r.status_code == 200:
        tokens[user['email']] = r.json()['access_token']

# 3) Consultar /me con admin
if "admin@example.com" in tokens:
    headers = {"Authorization": f"Bearer {tokens['admin@example.com']}"}
    r = requests.get(f"{BASE_URL}/me", headers=headers)
    print("/me admin", r.status_code, r.text)

# 4) Obtener lista de usuarios administrables (admin)
if "admin@example.com" in tokens:
    headers = {"Authorization": f"Bearer {tokens['admin@example.com']}"}
    r = requests.get(f"{BASE_URL}/users", headers=headers)
    print("/users admin", r.status_code, r.text)

# 5) Intentar GET /users con employee (debería 403)
if "employee@example.com" in tokens:
    headers = {"Authorization": f"Bearer {tokens['employee@example.com']}"}
    r = requests.get(f"{BASE_URL}/users", headers=headers)
    print("/users employee", r.status_code, r.text)

# 6) Eliminar un usuario con admin (tomar ID del endpoint /users)
if "admin@example.com" in tokens:
    headers = {"Authorization": f"Bearer {tokens['admin@example.com']}"}
    r = requests.get(f"{BASE_URL}/users", headers=headers)
    if r.status_code == 200:
        users = r.json()
        employee = next((u for u in users if u['email'] == 'employee@example.com'), None)
        if employee:
            r2 = requests.delete(f"{BASE_URL}/users/{employee['id']}", headers=headers)
            print("delete employee (admin)", r2.status_code, r2.text)
        else:
            print("employee user no encontrado para borrar")
    else:
        print("No se pudo listar usuarios para borrar")

# 7) Ejecutar refresh token si quieres full flow
# Necesitas obtener el refresh_token del login response (actualiza este bloque si lo guardas)