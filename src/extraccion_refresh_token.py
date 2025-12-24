"""
Script que, dado tu cliente, secreto y código de autorización, devuelve el token de acceso (6h) y el token de refresco (permanente).
Sólo se usa una vez o en caso de pérdida del refresh token. 

Para poder encontrar el 'code', debes abrir 
http://www.strava.com/oauth/authorize?client_id=TUCLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read,activity:read_all

en tu navegador, aceptar los permisos, y copiar el código que aparece en la URL de redirección.
"""

import requests

# --- TUS DATOS ---
client_id = ""       
client_secret = "" # Se encuentra en la API de Strava.
code = "" # El código que obtuviste al autorizar la app.

# Hacemos el canje
print("🔄 Canjeando código por token...")

response = requests.post(
    url='https://www.strava.com/oauth/token',
    data={
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
)

datos = response.json()

if response.status_code == 200:
    print("\n✅ ¡ÉXITO! Aquí están tus credenciales reales:\n")
    print(f"ACCESS TOKEN (Para usar YA): {datos['access_token']}")
    print(f"REFRESH TOKEN (Para el futuro): {datos['refresh_token']}")
    print(f"Caduca en: {datos['expires_in']} segundos")
    print("\n---> COPIA EL 'ACCESS TOKEN' Y ÚSALO EN TU SCRIPT DE INFLUXDB <---")
else:
    print("\n❌ Error al canjear:")
    print(datos)