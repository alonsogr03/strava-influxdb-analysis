# Proyecto Final - Análisis de Datos de Strava con InfluxDB y Grafana

Proyecto de Big Data Preprocessing I - Extracción, almacenamiento y análisis de datos de actividades deportivas de Strava.

**Autores:** Alba Martínez de la Hermosa y Alonso González romero

---

## 📋 Descripción

Este proyecto permite:
- Conectarse a la API de Strava mediante tokens personalizados
- Extraer datos de actividades deportivas
- Almacenar los datos localmente y en InfluxDB
- Realizar consultas y análisis sobre los datos
- Visualizar métricas a través de Grafana
- Empaquetar todo el sistema con Docker

---

## 🗂️ Estructura del Proyecto

```
Trabajo-Final/
├── data/                    # Datos extraídos de Strava (JSON)
├── docker/                  # Configuración de Docker
│   └── docker-compose.yml  # Servicios: InfluxDB + Grafana
├── notebooks/               # Documentación y análisis
│   └── memoria_consultas.qmd
├── src/                     # Código fuente
│   └── main.py             # Script principal
├── .env.example            # Ejemplo de variables de entorno
├── .gitignore
├── requirements.txt        # Dependencias de Python
└── README.md
```

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Trabajo-Final
```

### 2. Crear entorno virtual de Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus credenciales
```

Necesitarás configurar:
- **Tokens de Strava**: Para Alba y Alonso (obtenerlos desde [Strava API](https://www.strava.com/settings/api))
- **Credenciales de InfluxDB**: Token, organización y bucket
- **Credenciales de Grafana**: Usuario y contraseña

### 5. Iniciar servicios con Docker

```bash
cd docker
docker-compose up -d
```

Esto iniciará:
- **InfluxDB** en `http://localhost:8086`
- **Grafana** en `http://localhost:3000`

---

## 💻 Uso del Sistema

### Ejecutar el script principal

```bash
python src/main.py
```

El script te guiará a través de los siguientes pasos:

1. **Seleccionar usuario** (Alba o Alonso)
2. **Ingresar ID de actividad** de Strava
3. **Especificar tipo de actividad** (Run, Ride, Swim, etc.)

El script automáticamente:
- Extraerá los datos de Strava
- Guardará los datos en `data/`
- Subirá los datos a InfluxDB

### Ejemplo de ejecución

```
=== SISTEMA DE CARGA DE DATOS STRAVA ===

Selecciona el usuario:
1. Alba
2. Alonso

Ingresa el número (1 o 2): 1

✓ Usuario seleccionado: Alba
✓ Conectado a Strava como Alba

Ingresa el ID de la actividad de Strava: 123456789

Tipo de actividad:
Ejemplos: Run, Ride, Swim, Hike, Walk, etc.
Ingresa el tipo de actividad: Run

⏳ Obteniendo datos de la actividad 123456789...
✓ Actividad obtenida: Morning Run
  - Tipo: Run
  - Distancia: 5.23 km
  - Tiempo: 28 minutos

✓ Datos guardados localmente en: data/activity_123456789_Alba.json
⏳ Subiendo datos a InfluxDB...
✓ Datos subidos correctamente a InfluxDB

✓ Proceso completado exitosamente!
```

---

## 📊 Visualización con Grafana

1. Accede a Grafana: `http://localhost:3000`
2. Login con las credenciales configuradas en `.env`
3. Añadir InfluxDB como fuente de datos:
   - URL: `http://influxdb:8086`
   - Organization: valor de `INFLUX_ORG`
   - Token: valor de `INFLUX_TOKEN`
   - Bucket: valor de `INFLUX_BUCKET`
4. Crear dashboards para visualizar las métricas

---

## 📝 Consultas y Análisis

Las consultas se documentan en el archivo Quarto:

```bash
# Abrir y editar el archivo
notebooks/memoria_consultas.qmd
```

Para renderizar el documento:

```bash
quarto render notebooks/memoria_consultas.qmd
```

---

## 🔧 Obtener Token de Strava

1. Ir a [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Crear una aplicación
3. Obtener `Client ID` y `Client Secret`
4. Generar token de acceso usando OAuth2

Más información: [Strava API Documentation](https://developers.strava.com/docs/getting-started/)

---

## 🐳 Comandos Docker Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (¡cuidado, borra los datos!)
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart influxdb
```

---

## 📦 Dependencias Principales

- **stravalib**: Cliente de Python para Strava API
- **influxdb-client**: Cliente para InfluxDB 2.x
- **pandas**: Manipulación de datos
- **python-dotenv**: Gestión de variables de entorno
- **requests**: Peticiones HTTP

---

## 🔄 Flujo de Datos

```
Strava API
    ↓
main.py (extracción)
    ↓
data/ (almacenamiento local)
    ↓
InfluxDB (base de datos temporal)
    ↓
Grafana (visualización)
```

---

## 📚 Recursos Adicionales

- [Documentación de Strava API](https://developers.strava.com/)
- [Documentación de InfluxDB](https://docs.influxdata.com/)
- [Documentación de Grafana](https://grafana.com/docs/)
- [Quarto Documentation](https://quarto.org/)

---

## 📄 Licencia

Este proyecto es parte del trabajo final de la asignatura Big Data Preprocessing I.

---

