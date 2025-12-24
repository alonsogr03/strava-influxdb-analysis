"""
Script para consultar y verificar datos en InfluxDB
Autores: Alba y Alonso
Fecha: 2025-12-24
"""

import os
from dotenv import load_dotenv
from influxdb_client_3 import InfluxDBClient3
import pandas as pd

# Cargar variables de entorno1
load_dotenv()


def listar_measurements(client, database):
    """
    Lista todos los measurements (tablas) disponibles en la base de datos.
    """
    query = f"""
    SHOW MEASUREMENTS
    """
    try:
        table = client.query(query=query, database=database, language='influxql')
        df = table.to_pandas()
        return df
    except Exception as e:
        print(f"❌ Error al listar measurements: {e}")
        return None


def consultar_datos(client, measurement, database, limit=None):
    """
    Consulta todos los datos de un measurement específico.
    """
    if limit:
        query = f"""
        SELECT * FROM "{measurement}"
        ORDER BY time DESC
        LIMIT {limit}
        """
    else:
        query = f"""
        SELECT * FROM "{measurement}"
        ORDER BY time DESC
        """
    
    try:
        print(f"\n⏳ Consultando datos de la tabla '{measurement}'...")
        table = client.query(query=query, database=database, language='influxql')
        df = table.to_pandas()
        print(f"✅ Se encontraron {len(df)} registros")
        return df
    except Exception as e:
        print(f"❌ Error al consultar datos: {e}")
        return None


def consultar_por_usuario(client, measurement, usuario, database, limit=None):
    """
    Consulta datos filtrados por usuario.
    """
    if limit:
        query = f"""
        SELECT * FROM "{measurement}"
        WHERE "usuario" = '{usuario}'
        ORDER BY time DESC
        LIMIT {limit}
        """
    else:
        query = f"""
        SELECT * FROM "{measurement}"
        WHERE "usuario" = '{usuario}'
        ORDER BY time DESC
        """
    
    try:
        print(f"\n⏳ Consultando datos de {usuario} en '{measurement}'...")
        table = client.query(query=query, database=database, language='influxql')
        df = table.to_pandas()
        print(f"✅ Se encontraron {len(df)} registros")
        return df
    except Exception as e:
        print(f"❌ Error al consultar datos: {e}")
        return None


def consultar_por_actividad(client, measurement, id_actividad, database):
    """
    Consulta datos de una actividad específica.
    """
    query = f"""
    SELECT * FROM "{measurement}"
    WHERE "id_actividad" = '{id_actividad}'
    ORDER BY time DESC
    """
    
    try:
        print(f"\n⏳ Consultando actividad {id_actividad} en '{measurement}'...")
        table = client.query(query=query, database=database, language='influxql')
        df = table.to_pandas()
        print(f"✅ Se encontraron {len(df)} registros")
        return df
    except Exception as e:
        print(f"❌ Error al consultar datos: {e}")
        return None


def estadisticas_base_datos(client, database):
    """
    Muestra estadísticas generales de la base de datos.
    """
    print("\n" + "="*60)
    print("   ESTADÍSTICAS DE LA BASE DE DATOS")
    print("="*60 + "\n")
    
    measurements = ['Run', 'Cycling', 'Swimming']
    
    for measurement in measurements:
        query = f"""
        SELECT COUNT(*) FROM "{measurement}"
        """
        try:
            table = client.query(query=query, database=database, language='influxql')
            df = table.to_pandas()
            if not df.empty:
                count = df.iloc[0]['count']
                print(f"📊 {measurement}: {count} registros")
        except:
            print(f"📊 {measurement}: 0 registros (tabla vacía o no existe)")
    
    print("\n" + "="*60)


def main():
    """
    Función principal del script de consultas
    """
    print("\n" + "="*60)
    print("   SISTEMA DE CONSULTA DE DATOS EN InfluxDB")
    print("="*60 + "\n")
    
    # Obtener configuración de InfluxDB desde variables de entorno
    influx_host = os.getenv('INFLUX_HOST')
    influx_token = os.getenv('INFLUX_TOKEN')
    influx_org = os.getenv('INFLUX_ORG')
    influx_database = os.getenv('INFLUX_DATABASE')
    
    if not all([influx_host, influx_token, influx_org, influx_database]):
        print("❌ Error: Faltan credenciales de InfluxDB en las variables de entorno")
        print("   Variables necesarias: INFLUX_HOST, INFLUX_TOKEN, INFLUX_ORG, INFLUX_DATABASE")
        return
    
    # Crear conexión a InfluxDB
    try:
        client = InfluxDBClient3(host=influx_host, token=influx_token, org=influx_org, database=influx_database)
        print("✅ Conectado a InfluxDB exitosamente\n")
    except Exception as e:
        print(f"❌ Error al conectar con InfluxDB: {e}")
        return
    
    # Mostrar estadísticas generales
    estadisticas_base_datos(client, influx_database)
    
    # Menú de opciones
    while True:
        print("\n📋 Opciones de Consulta:")
        print("1. Consultar tabla Run")
        print("2. Consultar tabla Cycling")
        print("3. Consultar tabla Swimming")
        print("4. Consultar por usuario específico")
        print("5. Consultar por ID de actividad")
        print("6. Ver estadísticas actualizadas")
        print("7. Salir")
        
        opcion = input("\nSelecciona una opción (1-7): ").strip()
        
        if opcion == '1':
            limit_str = input("¿Cuántos registros quieres ver? (Enter para todos): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            df = consultar_datos(client, 'Run', influx_database, limit)
            if df is not None and not df.empty:
                print("\n" + "="*60)
                print(f"📊 Primeros registros de Run:")
                print("="*60)
                print(df.head(20))
                print("\n📈 Resumen:")
                print(df.info())
                
        elif opcion == '2':
            limit_str = input("¿Cuántos registros quieres ver? (Enter para todos): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            df = consultar_datos(client, 'Cycling', influx_database, limit)
            if df is not None and not df.empty:
                print("\n" + "="*60)
                print(f"📊 Primeros registros de Cycling:")
                print("="*60)
                print(df.head(20))
                print("\n📈 Resumen:")
                print(df.info())
                
        elif opcion == '3':
            limit_str = input("¿Cuántos registros quieres ver? (Enter para todos): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            df = consultar_datos(client, 'Swimming', influx_database, limit)
            if df is not None and not df.empty:
                print("\n" + "="*60)
                print(f"📊 Primeros registros de Swimming:")
                print("="*60)
                print(df.head(20))
                print("\n📈 Resumen:")
                print(df.info())
                
        elif opcion == '4':
            print("\n👤 Selecciona el usuario:")
            print("1. Alba")
            print("2. Alonso")
            user_opcion = input("Selecciona 1 o 2: ").strip()
            usuario = 'Alba' if user_opcion == '1' else 'Alonso'
            
            print("\n🏃 Selecciona el tipo de actividad:")
            print("1. Run")
            print("2. Cycling")
            print("3. Swimming")
            tipo_opcion = input("Selecciona 1, 2 o 3: ").strip()
            measurement = {'1': 'Run', '2': 'Cycling', '3': 'Swimming'}.get(tipo_opcion, 'Run')
            
            limit_str = input("¿Cuántos registros quieres ver? (Enter para todos): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            
            df = consultar_por_usuario(client, measurement, usuario, influx_database, limit)
            if df is not None and not df.empty:
                print("\n" + "="*60)
                print(f"📊 Datos de {usuario} en {measurement}:")
                print("="*60)
                print(df.head(20))
                print("\n📈 Resumen:")
                print(df.info())
                
        elif opcion == '5':
            activity_id = input("\n🔢 Ingresa el ID de la actividad: ").strip()
            
            print("\n🏃 Selecciona el tipo de actividad:")
            print("1. Run")
            print("2. Cycling")
            print("3. Swimming")
            tipo_opcion = input("Selecciona 1, 2 o 3: ").strip()
            measurement = {'1': 'Run', '2': 'Cycling', '3': 'Swimming'}.get(tipo_opcion, 'Run')
            
            df = consultar_por_actividad(client, measurement, activity_id, influx_database)
            if df is not None and not df.empty:
                print("\n" + "="*60)
                print(f"📊 Datos de la actividad {activity_id}:")
                print("="*60)
                print(df.head(20))
                print("\n📈 Resumen:")
                print(df.info())
                
                # Ofrecer exportar a CSV
                exportar = input("\n¿Exportar estos datos a CSV? (S/N): ").strip().upper()
                if exportar == 'S':
                    filename = f"data/consulta_actividad_{activity_id}.csv"
                    os.makedirs("data", exist_ok=True)
                    df.to_csv(filename, index=False)
                    print(f"✅ Datos exportados a: {filename}")
                
        elif opcion == '6':
            estadisticas_base_datos(client, influx_database)
            
        elif opcion == '7':
            print("\n👋 ¡Hasta pronto!")
            break
            
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
    
    # Cerrar conexión
    client.close()
    print("\n" + "="*60)
    print("   Conexión cerrada")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Proceso interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
