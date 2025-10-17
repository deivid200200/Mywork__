# Mi Primer Proyecto Data Engineer

Este es mi primer proyecto completo de Data Engineering, implementando un pipeline de datos end-to-end usando herramientas gratuitas y estándar del mercado, con Python como lenguaje principal.

## Stack Tecnológico
- **Python 3.13** (lenguaje principal)
- **SQLite** (base de datos local)
- **Streamlit** (dashboard interactivo)
- **Requests** (descarga de datos)
- **CSV + SQLite3** (procesamiento nativo de Python)

## Arquitectura del Pipeline
1. **Ingesta**: Descarga automática de dataset público (Uber rides)
2. **Validación**: Verificación básica de estructura y calidad de datos
3. **Transformación**: Limpieza y procesamiento (muestra de 100 registros)
4. **Almacenamiento**: Carga en base de datos SQLite local
5. **Visualización**: Dashboard web con Streamlit

## Estructura del Proyecto
```
dataengineer1st/
├── data/
│   ├── raw/                    # Datos originales descargados
│   ├── processed/              # Datos transformados
│   └── warehouse/              # Base de datos SQLite
├── src/
│   ├── ingest/                 # Módulo de ingesta de datos
│   ├── quality/                # Validaciones de calidad
│   ├── transform/              # Transformaciones de datos
│   ├── warehouse/              # Carga a base de datos
│   └── orchestrate/            # Pipeline principal
├── dash/                       # Dashboard de Streamlit
├── tests/                      # Pruebas automatizadas
└── requirements.txt            # Dependencias del proyecto
```

## Cómo Ejecutar el Proyecto

### 1. Configuración del Entorno
```powershell
# Crear entorno virtual
py -m venv .venv

# Activar entorno
.\.venv\Scripts\Activate.ps1

# O cambiar política de ejecución
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 2. Instalar Dependencias
```powershell
# Instalar paquetes necesarios
.\.venv\Scripts\python -m pip install requests streamlit
```

### 3. Ejecutar Pipeline de Datos
```powershell
# Correr el pipeline completo (descarga, procesa y carga datos)
.\.venv\Scripts\python -m src.orchestrate.flow
```

### 4. Lanzar Dashboard
```powershell
# Abrir dashboard interactivo en el navegador
.\.venv\Scripts\streamlit run dash/app.py
```

## Resultados del Pipeline
- **Datos procesados**: 1,511,443 registros de viajes de Uber
- **Muestra analizada**: 100 registros para demostración
- **Columnas**: Date/Time, Lat, Lon
- **Base de datos**: SQLite con tabla `staging_trips`

## Características Implementadas
-  **Ingesta automatizada** de datos públicos
-  **Validación de calidad** básica
-  **Transformación** y limpieza de datos
-  **Almacenamiento** en base de datos local
-  **Dashboard interactivo** con métricas
-  **Código en español** para facilitar comprensión
-  **Arquitectura modular** y escalable





