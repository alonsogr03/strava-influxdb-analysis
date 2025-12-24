# 📖 Guía de Uso - Script de Carga Strava → InfluxDB

## 🎯 Descripción

Este script permite descargar datos de actividades desde Strava y cargarlos automáticamente en InfluxDB, con soporte para múltiples usuarios (Alba y Alonso) y diferentes tipos de actividades (Run, Cycling, Swimming).

## 🔧 Configuración Inicial

### 1. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y rellena con tus credenciales:

```powershell
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales reales:

- **Para cada usuario (Alba y Alonso):**
  - `STRAVA_CLIENT_ID_[USUARIO]`: ID de tu aplicación Strava
  - `STRAVA_CLIENT_SECRET_[USUARIO]`: Secret de tu aplicación Strava
  - `STRAVA_REFRESH_TOKEN_[USUARIO]`: Token de refresco de Strava

- **Para InfluxDB:**
  - `INFLUX_HOST`: URL de tu servidor InfluxDB (ej: `https://us-east-1-1.aws.cloud2.influxdata.com`)
  - `INFLUX_TOKEN`: Token de autenticación de InfluxDB
  - `INFLUX_ORG`: Nombre de tu organización en InfluxDB
  - `INFLUX_DATABASE`: Nombre de la base de datos/bucket

## 🚀 Uso del Script

### Ejecutar el Script Principal

```powershell
python src/main.py
```

### Flujo del Script

El script te guiará paso a paso:

1. **Selección de Usuario**
   - Elige si eres Alba (opción 1) o Alonso (opción 2)

2. **Autenticación Automática**
   - El script generará automáticamente un token de acceso válido

3. **Número de Actividad**
   - Introduce el ID de la actividad de Strava (lo puedes encontrar en la URL de Strava)
   - Ejemplo: En `https://www.strava.com/activities/12345678`, el ID es `12345678`

4. **Tipo de Actividad**
   - Selecciona el tipo:
     - 1 = Run (Correr)
     - 2 = Cycling (Ciclismo)
     - 3 = Swimming (Natación)

5. **Revisión de Datos**
   - El script descargará los datos y los guardará en un CSV en la carpeta `data/`
   - Verás una vista previa de los primeros registros
   - **IMPORTANTE**: Revisa el archivo CSV para verificar que los datos sean correctos

6. **Confirmación de Carga**
   - El script preguntará: `¿Subes el archivo a InfluxDB? (S/N)`
   - Si respondes **S**: Los datos se subirán a InfluxDB en la tabla correspondiente
   - Si respondes **N**: Los datos quedarán guardados localmente sin subir

## 📊 Estructura de Datos

### CSV Generado

El script genera dos archivos CSV:

1. **CSV Original**: `data/strava_activity_[ID].csv`
   - Datos crudos tal como vienen de Strava

2. **CSV Modificado**: `data/strava_activity_[ID]_modificado.csv`
   - Incluye columnas adicionales:
     - `usuario`: Alba o Alonso
     - `id_actividad`: ID de la actividad
     - `tipo_actividad`: Run, Cycling o Swimming

### Columnas Disponibles

Dependiendo de la actividad, el CSV puede incluir:

- `timestamp_real`: Fecha y hora del registro
- `time`: Tiempo en segundos desde el inicio
- `distance`: Distancia en metros
- `latitude` / `longitude`: Coordenadas GPS
- `altitude`: Altitud en metros
- `velocity_smooth`: Velocidad suavizada
- `heartrate`: Frecuencia cardíaca
- `cadence`: Cadencia (pasos/min o RPM)
- `watts`: Potencia en vatios
- `temp`: Temperatura
- `grade_smooth`: Pendiente suavizada

## 🏷️ Tablas en InfluxDB

Los datos se organizan por tipo de actividad:

- **Run**: Actividades de carrera
- **Cycling**: Actividades de ciclismo
- **Swimming**: Actividades de natación

Cada tabla incluye los siguientes **tags** (para filtrado eficiente):
- `usuario`: Alba o Alonso
- `id_actividad`: ID único de la actividad
- `tipo_actividad`: Tipo de actividad

## ⚠️ Solución de Problemas

### Error: "Faltan credenciales de Strava"
- Verifica que el archivo `.env` existe y está en el directorio raíz del proyecto
- Asegúrate de que todas las variables `STRAVA_*` están definidas para el usuario seleccionado

### Error: "No se pudo obtener el token de acceso"
- Verifica que el `REFRESH_TOKEN` es válido y no ha expirado
- Comprueba que el `CLIENT_ID` y `CLIENT_SECRET` son correctos

### Error: "Faltan credenciales de InfluxDB"
- Verifica que todas las variables `INFLUX_*` están definidas en el archivo `.env`
- Comprueba que tienes permisos de escritura en la base de datos

### Error: "Esta actividad no tiene datos de tiempo"
- La actividad puede ser manual (sin GPS)
- Intenta con una actividad que tenga datos de GPS/sensores

## 📝 Ejemplo de Ejecución

```
============================================================
   SISTEMA DE CARGA DE DATOS STRAVA → InfluxDB
============================================================

👤 ¿Quién eres?
1. Alba
2. Alonso

Selecciona 1 o 2: 1

✅ Usuario seleccionado: Alba
🔄 Refrescando token de Strava para Alba...
✅ Token renovado exitosamente para Alba

🔢 Ingresa el número de actividad de Strava: 12345678

🏃 ¿Qué tipo de actividad es?
1. Run (Correr)
2. Cycling (Ciclismo)
3. Swimming (Natación)

Selecciona 1, 2 o 3: 1
✅ Tipo de actividad: Run

⏳ Descargando datos de la actividad 12345678...
⏳ Conectando con Strava para actividad 12345678...
✅ Archivo guardado exitosamente: data/strava_activity_12345678.csv

📊 Vista previa de los datos (primeras 5 filas):
[...]

⚠️  Por favor, revisa el archivo: data/strava_activity_12345678.csv
    Asegúrate de que los datos son correctos antes de subirlos.

¿Subes el archivo a InfluxDB? (S/N): S

✅ CSV modificado guardado: data/strava_activity_12345678_modificado.csv
⏳ Subiendo datos a InfluxDB en la tabla 'Run'...
✅ Datos subidos exitosamente a InfluxDB (tabla: Run)

🎉 ¡Proceso completado exitosamente!
   - Usuario: Alba
   - Actividad: 12345678
   - Tipo: Run
   - Registros: 1523

============================================================
   Gracias por usar el sistema
============================================================
```

## 👥 Autores

- Alba
- Alonso

## 📅 Fecha

Diciembre 2025
