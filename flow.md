# EcoTrackLite Backend - Guía de Configuración Inicial

Esta guía detalla los pasos necesarios para poner en marcha el proyecto después de clonar el repositorio.

## 1. Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## 2. Configuración del Entorno Virtual

Crea un entorno virtual para aislar las dependencias del proyecto:

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

## 3. Instalación de Dependencias

Instala todas las librerías necesarias especificadas en el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 4. Variables de Entorno

El proyecto utiliza variables de entorno para la configuración. Copia el archivo de ejemplo y ajusta si es necesario:

```bash
cp .env.example .env
```

*Por defecto, `.env` está configurado para usar SQLite localmente.*

## 5. Inicialización de la Base de Datos y Datos de Prueba

Ejecuta el script de "seed" para crear las tablas y cargar datos iniciales (categorías escolares, un colegio de prueba, un residuo y una alerta):

```bash
python3 seed.py
```

## 6. Ejecución del Servidor de Desarrollo

Inicia el servidor con recarga automática para empezar a trabajar:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Puedes acceder a la documentación interactiva (Swagger) en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 7. Ejecución de Pruebas (Opcional)

Para verificar que todo está funcionando correctamente, puedes ejecutar la suite de tests:

```bash
pytest
```

## Credenciales de Prueba (Cargadas mediante seed.py)
- **Usuario**: `san.idelfonso@edu.es`
- **Password**: `colegio2026`
