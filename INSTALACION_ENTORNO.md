# 🔧 Instalación del Entorno Virtual - Paso a Paso

Este documento explica cómo configurar el entorno virtual Python desde cero para el proyecto de carga de datos Strava → InfluxDB.

## 📋 Requisitos Previos

- Python 3.13 o superior instalado
- Terminal PowerShell
- Acceso al directorio del proyecto

## 🚀 Pasos de Instalación

### Eliminar el Entorno Virtual Antiguo

Como creamos ya un entorno, vamos a eliminarlo:

```powershell
Remove-Item -Path "venv" -Recurse -Force
```

⚠️ **Nota**: Este comando eliminará completamente la carpeta `venv`. Asegúrate de estar en el directorio correcto.

### Crear un Nuevo Entorno Virtual

Crea un entorno virtual limpio:

```powershell
python -m venv venv
```

Este comando creará una nueva carpeta `venv` con un entorno Python aislado.

### 4. Activar el Entorno Virtual

Activa el entorno virtual recién creado:

```powershell
& "venv\Scripts\Activate.ps1"
```

Deberías ver `(venv)` al inicio de tu línea de comando, indicando que el entorno está activo.

### 5. Actualizar pip

Actualiza pip a la última versión:

```powershell
python -m pip install --upgrade pip
```

Esto asegura que tengas la última versión del gestor de paquetes.

### 6. Instalar las Dependencias

Instala todas las librerías necesarias desde el archivo `requirements.txt`:

```powershell
pip install -r requirements.txt
```

Este proceso instalará:
- `requests` - Para llamadas a la API de Strava
- `influxdb3-python` - Para conexión con InfluxDB
- `pandas` - Para manipulación de datos
- `numpy` - Para operaciones numéricas
- `python-dotenv` - Para cargar variables de entorno
- `matplotlib`, `seaborn`, `plotly` - Para visualización (opcional)

### 7. Verificar la Instalación

Verifica que no haya conflictos de dependencias:

```powershell
pip list
```

Deberías ver todas las librerías instaladas sin mensajes de error.

## ✅ Confirmación de Éxito

Si todo ha ido bien, deberías ver algo como:

```
Successfully installed certifi-2025.11.12 charset-normalizer-3.4.4 contourpy-1.3.3 
cycler-0.12.1 fonttools-4.61.1 idna-3.11 influxdb3-python-0.16.0 kiwisolver-1.4.9 
matplotlib-3.10.8 narwhals-2.14.0 numpy-2.4.0 packaging-25.0 pandas-2.3.3 
pillow-12.0.0 plotly-6.5.0 pyarrow-22.0.0 pyparsing-3.3.1 python-dateutil-2.8.2 
python-dotenv-1.0.0 pytz-2025.2 reactivex-4.1.0 requests-2.31.0 seaborn-0.13.2 
six-1.17.0 typing-extensions-4.15.0 tzdata-2025.3 urllib3-2.6.2
```

Feliz navidad :)

## 📅 Última Actualización
24 de diciembre de 2025
