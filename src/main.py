"""
Script principal para extraer datos de Strava y cargarlos en InfluxDB
Autores: Alba y Alonso
Fecha: 2025-12-24
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from influxdb_client_3 import InfluxDBClient3

# Cargar variables de entorno
load_dotenv()


def obtener_token_acceso(client_id, client_secret, refresh_token, usuario):
    """
    Obtiene un access token válido usando el refresh token.
    Basado en crear_token_refresco.py
    """
    print(f"🔄 Refrescando token de Strava para {usuario}...")
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'f': 'json'
    }
    
    try:
        res = requests.post(auth_url, data=payload, verify=False)
        res.raise_for_status()
        access_token = res.json()['access_token']
        print(f"✅ Token renovado exitosamente para {usuario}")
        return access_token
    except Exception as e:
        print(f"❌ Error al refrescar token: {e}")
        return None


def descargar_datos_actividad(activity_id, access_token):
    """
    Descarga todos los datos (streams) de una actividad de Strava.
    Basado en pruebas.py
    """
    # 1. Solicitamos TODOS los streams posibles
    keys = "time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,watts,temp,grade_smooth"
    url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys={keys}&key_by_type=true"
    
    headers = {'Authorization': f"Bearer {access_token}"}
    print(f"⏳ Conectando con Strava para actividad {activity_id}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error al descargar actividad: {response.text}")
        return None

    streams = response.json()
    
    # 2. Verificar que hay datos de tiempo
    if 'time' not in streams:
        print("❌ Esta actividad no tiene datos de tiempo (quizás es manual).")
        return None

    data_dict = {}
    
    # 3. Convertir los streams en un diccionario
    for key, value in streams.items():
        if key == 'latlng':
            # Separar latitud y longitud
            lats = [x[0] for x in value['data']]
            lngs = [x[1] for x in value['data']]
            data_dict['latitude'] = lats
            data_dict['longitude'] = lngs
        else:
            data_dict[key] = value['data']

    # 4. Crear DataFrame
    df = pd.DataFrame(data_dict)
    
    # 5. Obtener información adicional de la actividad (fecha de inicio)
    url_act = f"https://www.strava.com/api/v3/activities/{activity_id}"
    resp_act = requests.get(url_act, headers=headers).json()
    start_date = datetime.strptime(resp_act['start_date'], "%Y-%m-%dT%H:%M:%SZ")
    
    # 6. Calcular timestamps reales
    df['timestamp_real'] = df['time'].apply(lambda x: start_date + timedelta(seconds=x))
    
    # 7. Reordenar columnas
    cols = ['timestamp_real', 'time'] + [c for c in df.columns if c not in ['timestamp_real', 'time']]
    df = df[cols]

    return df


def guardar_csv(df, activity_id, data_path="data/"):
    """
    Guarda el DataFrame en un archivo CSV.
    """
    os.makedirs(data_path, exist_ok=True)
    nombre_archivo = f"{data_path}strava_activity_{activity_id}.csv"
    df.to_csv(nombre_archivo, index=False)
    print(f"✅ Archivo guardado exitosamente: {nombre_archivo}")
    return nombre_archivo


def preparar_csv_para_influx(archivo_csv, usuario, id_actividad, tipo_actividad):
    """
    Modifica el CSV añadiendo columnas de usuario, id_actividad, tipo_actividad y measurement.
    """
    df = pd.read_csv(archivo_csv)
    
    # Añadir columnas necesarias
    df['measurement'] = tipo_actividad  # Nombre de la tabla/measurement en InfluxDB
    df['usuario'] = usuario
    df['id_actividad'] = id_actividad
    df['tipo_actividad'] = tipo_actividad
    
    # Guardar el CSV modificado
    archivo_modificado = archivo_csv.replace('.csv', '_modificado.csv')
    df.to_csv(archivo_modificado, index=False)
    print(f"✅ CSV modificado guardado: {archivo_modificado}")
    return archivo_modificado


def subir_a_influxdb(archivo_csv, tipo_actividad, host, token, org, database):
    """
    Sube el CSV a InfluxDB en la tabla correspondiente según el tipo de actividad.
    Usa influxdb_client_3.
    """
    try:
        # Crear la conexión a InfluxDB
        client = InfluxDBClient3(host=host, token=token, org=org, database=database)
        
        # Determinar las columnas que son tags
        tag_columns = ["measurement", "usuario", "id_actividad", "tipo_actividad"]
        
        # Subir el archivo
        print(f"⏳ Subiendo datos a InfluxDB en la tabla '{tipo_actividad}'...")
        client.write_file(
            file=archivo_csv,
            tag_columns=tag_columns,
            timestamp_column="timestamp_real",
            data_format="csv"
        )
        
        print(f"✅ Datos subidos exitosamente a InfluxDB (tabla: {tipo_actividad})")
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al subir datos a InfluxDB: {e}")
        return False


def main():
    """
    Función principal del script
    """
    print("\n" + "="*60)
    print("   SISTEMA DE CARGA DE DATOS STRAVA → InfluxDB")
    print("="*60 + "\n")
    
    # Paso 1: Preguntar quién es
    print("👤 ¿Quién eres?")
    print("1. Alba")
    print("2. Alonso")
    
    while True:
        opcion = input("\nSelecciona 1 o 2: ").strip()
        if opcion == '1':
            usuario = 'Alba'
            break
        elif opcion == '2':
            usuario = 'Alonso'
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
    
    print(f"\n✅ Usuario seleccionado: {usuario}")
    
    if usuario == 'Alba':
        print("\n" + "🎄" * 30)
        print("   Hola Alba, soy Alonso!")
        print("   🎅 ¡Feliz Navidad! 🎅")
        print("   Seguramente esté pensando en el gofre que me debes :)")
        print("🎄" * 30 + "\n")
    
    # Configuración de credenciales desde variables de entorno
    usuarios_config = {
        'Alba': {
            'client_id': os.getenv('STRAVA_CLIENT_ID_ALBA'),
            'client_secret': os.getenv('STRAVA_CLIENT_SECRET_ALBA'),
            'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN_ALBA')
        },
        'Alonso': {
            'client_id': os.getenv('STRAVA_CLIENT_ID_ALONSO'),
            'client_secret': os.getenv('STRAVA_CLIENT_SECRET_ALONSO'),
            'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN_ALONSO')
        }
    }
    
    config = usuarios_config[usuario]
    
    # Verificar que existen las credenciales
    if not all([config['client_id'], config['client_secret'], config['refresh_token']]):
        print(f"❌ Error: Faltan credenciales de Strava para {usuario} en las variables de entorno")
        return
    
    # Paso 2: Obtener token de acceso
    access_token = obtener_token_acceso(
        config['client_id'],
        config['client_secret'],
        config['refresh_token'],
        usuario
    )
    
    if not access_token:
        print("❌ No se pudo obtener el token de acceso. Abortando.")
        return
    
    # Paso 2b: Preguntar número de actividad
    activity_id = input("\n🔢 Ingresa el número de actividad de Strava: ").strip()
    
    if not activity_id.isdigit():
        print("❌ El ID de actividad debe ser un número.")
        return
    
    # Paso 3: Preguntar tipo de actividad
    print("\n🏃 ¿Qué tipo de actividad es?")
    print("1. Run (Correr)")
    print("2. Cycling (Ciclismo)")
    print("3. Swimming (Natación)")
    
    tipos_actividad = {
        '1': 'Run',
        '2': 'Cycling',
        '3': 'Swimming'
    }
    
    while True:
        opcion_tipo = input("\nSelecciona 1, 2 o 3: ").strip()
        if opcion_tipo in tipos_actividad:
            tipo_actividad = tipos_actividad[opcion_tipo]
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
    
    print(f"✅ Tipo de actividad: {tipo_actividad}")
    
    # Paso 4: Descargar datos de la actividad
    print(f"\n⏳ Descargando datos de la actividad {activity_id}...")
    df = descargar_datos_actividad(activity_id, access_token)
    
    if df is None:
        print("❌ No se pudieron descargar los datos de la actividad.")
        return
    
    # Guardar CSV original
    archivo_csv = guardar_csv(df, activity_id)
    
    # Mostrar preview
    print("\n📊 Vista previa de los datos (primeras 5 filas):")
    print(df.head())
    print(f"\n📈 Total de registros: {len(df)}")
    print(f"📋 Columnas disponibles: {', '.join(df.columns.tolist())}")
    
    # Paso 4b: Preguntar si revisar y subir
    print(f"\n⚠️  Por favor, revisa el archivo: {archivo_csv}")
    print("    Asegúrate de que los datos son correctos antes de subirlos.")
    
    while True:
        respuesta = input("\n¿Subes el archivo a InfluxDB? (S/N): ").strip().upper()
        if respuesta in ['S', 'N']:
            break
        else:
            print("❌ Por favor, responde S o N.")
    
    # Paso 5: Subir a InfluxDB si el usuario acepta
    if respuesta == 'S':
        # Preparar CSV con columnas adicionales
        archivo_modificado = preparar_csv_para_influx(
            archivo_csv,
            usuario,
            activity_id,
            tipo_actividad
        )
        
        # Obtener configuración de InfluxDB desde variables de entorno
        influx_host = os.getenv('INFLUX_HOST')
        influx_token = os.getenv('INFLUX_TOKEN')
        influx_org = os.getenv('INFLUX_ORG')
        influx_database = os.getenv('INFLUX_DATABASE')
        
        if not all([influx_host, influx_token, influx_org, influx_database]):
            print("❌ Error: Faltan credenciales de InfluxDB en las variables de entorno")
            print("   Variables necesarias: INFLUX_HOST, INFLUX_TOKEN, INFLUX_ORG, INFLUX_DATABASE")
            return
        
        # Subir a InfluxDB
        exito = subir_a_influxdb(
            archivo_modificado,
            tipo_actividad,
            influx_host,
            influx_token,
            influx_org,
            influx_database
        )
        
        if exito:
            print(f"\n🎉 ¡Proceso completado exitosamente!")
            print(f"   - Usuario: {usuario}")
            print(f"   - Actividad: {activity_id}")
            print(f"   - Tipo: {tipo_actividad}")
            print(f"   - Registros: {len(df)}")
        else:
            print("\n❌ Hubo un error al subir los datos a InfluxDB.")
    else:
        print("\n⏹️  Subida cancelada. Los datos están guardados localmente en:")
        print(f"   {archivo_csv}")
    
    print("\n" + "="*60)
    print("   Gracias por usar el sistema")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Proceso interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
