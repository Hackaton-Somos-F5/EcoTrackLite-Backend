# EcoTrackLite Backend

EcoTrackLite es una solución robusta diseñada para la gestión y seguimiento automatizado de residuos en centros educativos. Esta API permite monitorear el peso, volumen y estado de los materiales reciclables, proporcionando herramientas de análisis para optimizar la logística de reciclaje.

## 🚀 Características Principales

- **Gestión de Colegios**: Registro y consulta de centros educativos.
- **Autenticación Segura**: Sistema de credenciales (email/password) con hashing mediante Bcrypt.
- **Control de Residuos**: Registro detallado de entradas vinculadas a categorías escolares (Azul, Amarillo, Verde, Marrón, Gris, Rojo).
- **Resumen Global**: Endpoint dedicado para obtener los totales acumulados por tipo de residuo.
- **Alertas en Tiempo Real**: Sistema de monitoreo de umbrales con alertas activas dinámicas.
- **Dashboard de Estadísticas**: Cálculo automático de porcentaje de ocupación por colegio.
- **Validación Estricta**: Control de datos mediante Pydantic y restricciones en la base de datos.
- **Pruebas Automatizadas**: Suite completa de tests de integración para garantizar la estabilidad.

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Backend framework moderno y veloz.
- **SQLAlchemy**: ORM potente para el mapeo de datos.
- **SQLite**: Persistencia de datos local y eficiente.
- **Pydantic**: Serialización y validación exhaustiva de datos.
- **Passlib (Bcrypt)**: Seguridad avanzada para la gestión de contraseñas.
- **Pytest**: Framework de pruebas para asegurar la calidad del código.

## 📂 Estructura del Proyecto

```text
.
├── documentation/      # Documentación detallada de la API
├── models/             # Modelos de base de datos (Colegio, Residuo, Alerta)
├── routes/             # Controladores y endpoints de la API
├── schemas/            # Definiciones de datos Pydantic
├── services/           # Lógica de negocio y agregaciones
├── tests/              # Pruebas de integración automatizadas
├── TKA/                # Historias de usuario y seguimiento de tareas
├── database.py         # Configuración y sesión de SQLAlchemy
├── main.py             # Punto de entrada y registro de routers
└── requirements.txt    # Dependencias del proyecto
```

## ⚙️ Configuración Local

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd EcoTrackLite-Backend
   ```

2. **Entorno Virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalación de Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de Entorno:**
   ```bash
   cp .env.example .env
   ```

5. **Inicialización y Datos de Prueba (Seed):**
   ```bash
   python3 seed.py
   ```

6. **Ejecutar Servidor:**
   ```bash
   uvicorn main:app --reload
   ```
   - Accede a la API en: `http://127.0.0.1:8000`
   - Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

### 🔑 Credenciales de Prueba (Cargadas vía Seed)
- **Email**: `san.idelfonso@edu.es`
- **Password**: `colegio2026`

## 🧪 Pruebas Automatizadas

Para ejecutar los tests de integración y verificar el funcionamiento del sistema:

```bash
pytest tests/ -v
```

## 📖 Documentación de la API

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **Guía Detallada**: [Documentación de Endpoints](./documentation/api-documentation.md)

---
Desarrollado con ❤️ para el seguimiento ecológico educativo.
