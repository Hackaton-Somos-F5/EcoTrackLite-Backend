# EcoTrackLite API Documentation

Esta documentación detalla los endpoints disponibles en la API de EcoTrackLite-Backend.

## Información General
- **Base URL**: `http://localhost:8000`
- **Documentación Interactiva**: `/docs` (Swagger UI) o `/redoc` (ReDoc)

---

## 1. Colegios

### Registrar un Colegio
Registra un nuevo centro educativo en el sistema.

- **URL**: `/colegios/`
- **Método**: `POST`
- **Cuerpo de la Petición**:
    ```json
    {
      "nombre": "Nombre del Colegio",
      "direccion": "Calle ejemplo 123",
      "ciudad": "Madrid",
      "telefono": "600000000",
      "email": "colegio@ejemplo.com",
      "password": "passwordSeguro123"
    }
    ```
- **Respuesta Exitosa (201 Created)**:
    ```json
    {
      "id": 1,
      "nombre": "Nombre del Colegio",
      "direccion": "Calle ejemplo 123",
      "ciudad": "Madrid",
      "telefono": "600000000",
      "email": "colegio@ejemplo.com",
      "fecha_creacion": "2024-02-18T20:00:00Z"
    }
    ```

### Listar Colegios
Obtiene una lista paginada de todos los colegios registrados.

- **URL**: `/colegios/`
- **Método**: `GET`
- **Parámetros de Consulta**:
    - `skip` (int, opcional): Número de registros a omitir (default: 0).
    - `limit` (int, opcional): Límite de registros a devolver (default: 100).
- **Respuesta Exitosa (200 OK)**: Lista de objetos de colegio.

### Detalle de un Colegio
Obtiene la información detallada de un colegio específico por su ID.

- **URL**: `/colegios/{colegio_id}`
- **Método**: `GET`
- **Respuesta Exitosa (200 OK)**: Objeto de colegio.
- **Errores**: `404 Not Found` si el ID no existe.

### Estadísticas del Colegio (Dashboard)
Obtiene el resumen de generación de residuos y comparación con umbrales.

- **URL**: `/colegios/{colegio_id}/stats`
- **Método**: `GET`
- **Respuesta Exitosa (200 OK)**:
    ```json
    {
      "colegio_id": 1,
      "colegio_nombre": "Nombre del Colegio",
      "estadisticas": [
        {
          "tipo": "plastico",
          "total_kg": 15.5,
          "total_litros": 45.0,
          "umbral_litros": 100.0,
          "porcentaje_ocupacion": 45.0
        }
      ]
    }
    ```

---

## 2. Residuos

### Registrar Residuo
Registra una nueva entrada de residuos vinculada a un colegio.

- **URL**: `/colegios/{colegio_id}/residuos`
- **Método**: `POST`
- **Cuerpo de la Petición**:
    ```json
    {
      "tipo": "plastico",
      "peso_kg": 10.5,
      "volumen_litros": 30.0,
      "aula": "Aula 101"
    }
    ```
- **Respuesta Exitosa (201 Created)**: Objeto de residuo creado con `id`, `estado` ("pendiente") y `fecha_registro`.

### Consultar Residuos por Colegio
Lista los residuos de un colegio con opciones de filtrado.

- **URL**: `/colegios/{colegio_id}/residuos`
- **Método**: `GET`
- **Parámetros de Consulta**:
    - `tipo` (string, opcional): Filtrar por tipo (`plastico`, `papel`, `vidrio`, `organico`, `electronico`).
    - `estado` (string, opcional): Filtrar por estado (`pendiente`, `reciclado`).
- **Respuesta Exitosa (200 OK)**: Lista de objetos de residuo.

---

## 3. Autenticación

### Inicio de Sesión
Permite a un colegio autenticarse mediante su correo y contraseña.

- **URL**: `/auth/login`
- **Método**: `POST`
- **Cuerpo de la Petición**:
    ```json
    {
      "email": "colegio@ejemplo.com",
      "password": "passwordSeguro123"
    }
    ```
- **Respuesta Exitosa (200 OK)**:
    ```json
    {
      "message": "Inicio de sesión exitoso",
      "colegio_id": 1,
      "colegio_nombre": "Nombre del Colegio"
    }
    ```
- **Errores**: `401 Unauthorized` si las credenciales son incorrectas.

---

## 4. General

### Health Check
Verifica que el servicio esté activo.

- **URL**: `/`
- **Método**: `GET`
- **Respuesta**: `{"status": "ok"}`
