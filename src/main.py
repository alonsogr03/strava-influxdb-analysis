"""
Script principal para extraer datos de Strava y cargarlos en InfluxDB
Autores: Alba y Alonso
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from stravalib.client import Client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

# Cargar variables de entorno
load_dotenv()


class StravaToInfluxDB:
    """Clase para manejar la extracción de datos de Strava y carga a InfluxDB"""
    
    def __init__(self):
        """Inicializar conexiones con Strava e InfluxDB"""
        # Configuración de usuarios
        self.users = {
            'Alba': {
                'access_token': os.getenv('STRAVA_TOKEN_ALBA')
            },
            'Alonso': {
                'access_token': os.getenv('STRAVA_TOKEN_ALONSO')
            }
        }
        
        # Configuración de InfluxDB
        self.influx_url = os.getenv('INFLUX_URL', 'http://localhost:8086')
        self.influx_token = os.getenv('INFLUX_TOKEN')
        self.influx_org = os.getenv('INFLUX_ORG')
        self.influx_bucket = os.getenv('INFLUX_BUCKET')
        
        # Cliente de InfluxDB
        self.influx_client = InfluxDBClient(
            url=self.influx_url,
            token=self.influx_token,
            org=self.influx_org
        )
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
    
    def select_user(self):
        """Permite al usuario seleccionar su perfil"""
        print("\n=== SISTEMA DE CARGA DE DATOS STRAVA ===\n")
        print("Selecciona el usuario:")
        print("1. Alba")
        print("2. Alonso")
        
        while True:
            choice = input("\nIngresa el número (1 o 2): ").strip()
            if choice == '1':
                return 'Alba'
            elif choice == '2':
                return 'Alonso'
            else:
                print("Opción inválida. Intenta de nuevo.")
    
    def get_strava_client(self, user_name):
        """Crear cliente de Strava para el usuario seleccionado"""
        access_token = self.users[user_name]['access_token']
        
        if not access_token:
            raise ValueError(f"Token de acceso no configurado para {user_name}")
        
        client = Client(access_token=access_token)
        return client
    
    def get_activity_data(self, client, activity_id):
        """Obtener datos de una actividad específica de Strava"""
        try:
            activity = client.get_activity(activity_id)
            
            # Extraer datos relevantes
            activity_data = {
                'id': activity.id,
                'name': activity.name,
                'type': activity.type,
                'distance': float(activity.distance) if activity.distance else 0,
                'moving_time': int(activity.moving_time.total_seconds()) if activity.moving_time else 0,
                'elapsed_time': int(activity.elapsed_time.total_seconds()) if activity.elapsed_time else 0,
                'total_elevation_gain': float(activity.total_elevation_gain) if activity.total_elevation_gain else 0,
                'start_date': activity.start_date,
                'average_speed': float(activity.average_speed) if activity.average_speed else 0,
                'max_speed': float(activity.max_speed) if activity.max_speed else 0,
                'average_heartrate': float(activity.average_heartrate) if activity.average_heartrate else None,
                'max_heartrate': float(activity.max_heartrate) if activity.max_heartrate else None,
                'calories': float(activity.calories) if activity.calories else None,
            }
            
            return activity_data
        
        except Exception as e:
            print(f"Error al obtener actividad {activity_id}: {e}")
            return None
    
    def save_to_local(self, activity_data, user_name):
        """Guardar datos localmente en la carpeta data"""
        filename = f"data/activity_{activity_data['id']}_{user_name}.json"
        
        # Convertir datetime a string para JSON
        data_to_save = activity_data.copy()
        if 'start_date' in data_to_save:
            data_to_save['start_date'] = data_to_save['start_date'].isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Datos guardados localmente en: {filename}")
    
    def upload_to_influxdb(self, activity_data, user_name, activity_type):
        """Subir datos a InfluxDB"""
        try:
            # Crear punto de datos para InfluxDB
            point = Point("actividad_strava") \
                .tag("usuario", user_name) \
                .tag("tipo_actividad", activity_type) \
                .tag("activity_id", str(activity_data['id'])) \
                .tag("activity_name", activity_data['name']) \
                .field("distance", activity_data['distance']) \
                .field("moving_time", activity_data['moving_time']) \
                .field("elapsed_time", activity_data['elapsed_time']) \
                .field("elevation_gain", activity_data['total_elevation_gain']) \
                .field("average_speed", activity_data['average_speed']) \
                .field("max_speed", activity_data['max_speed']) \
                .time(activity_data['start_date'], WritePrecision.NS)
            
            # Añadir campos opcionales si existen
            if activity_data.get('average_heartrate'):
                point.field("average_heartrate", activity_data['average_heartrate'])
            if activity_data.get('max_heartrate'):
                point.field("max_heartrate", activity_data['max_heartrate'])
            if activity_data.get('calories'):
                point.field("calories", activity_data['calories'])
            
            # Escribir en InfluxDB
            self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point)
            print(f"✓ Datos subidos correctamente a InfluxDB")
            
        except Exception as e:
            print(f"✗ Error al subir datos a InfluxDB: {e}")
    
    def run(self):
        """Ejecutar el flujo principal del programa"""
        try:
            # Seleccionar usuario
            user_name = self.select_user()
            print(f"\n✓ Usuario seleccionado: {user_name}")
            
            # Obtener cliente de Strava
            client = self.get_strava_client(user_name)
            print(f"✓ Conectado a Strava como {user_name}")
            
            # Solicitar ID de actividad
            activity_id = input("\nIngresa el ID de la actividad de Strava: ").strip()
            
            # Solicitar tipo de actividad
            print("\nTipo de actividad:")
            print("Ejemplos: Run, Ride, Swim, Hike, Walk, etc.")
            activity_type = input("Ingresa el tipo de actividad: ").strip()
            
            print(f"\n⏳ Obteniendo datos de la actividad {activity_id}...")
            
            # Obtener datos de la actividad
            activity_data = self.get_activity_data(client, int(activity_id))
            
            if activity_data:
                print(f"\n✓ Actividad obtenida: {activity_data['name']}")
                print(f"  - Tipo: {activity_data['type']}")
                print(f"  - Distancia: {activity_data['distance']/1000:.2f} km")
                print(f"  - Tiempo: {activity_data['moving_time']//60} minutos")
                
                # Guardar localmente
                self.save_to_local(activity_data, user_name)
                
                # Subir a InfluxDB
                print(f"\n⏳ Subiendo datos a InfluxDB...")
                self.upload_to_influxdb(activity_data, user_name, activity_type)
                
                print(f"\n✓ Proceso completado exitosamente!")
            else:
                print(f"\n✗ No se pudieron obtener los datos de la actividad")
        
        except KeyboardInterrupt:
            print("\n\n✗ Proceso cancelado por el usuario")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        finally:
            # Cerrar conexión con InfluxDB
            self.influx_client.close()


if __name__ == "__main__":
    app = StravaToInfluxDB()
    app.run()
