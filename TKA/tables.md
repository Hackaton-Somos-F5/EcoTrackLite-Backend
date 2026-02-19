# TABLAS NECESARIAS

## 1. Tabla: colegios

**Nombre de la tabla:** `colegios`

**Campos:**

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT  
- `nombre`: VARCHAR(150), NOT NULL  
- `direccion`: VARCHAR(200), NOT NULL  
- `ciudad`: VARCHAR(100), NOT NULL  
- `telefono`: VARCHAR(20), NOT NULL  
- `email`: VARCHAR(150), NOT NULL, UNIQUE
- `password`: VARCHAR(255), NOT NULL
- `fecha_creacion`: DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP  

---

## 2. Tabla: residuos

**Nombre de la tabla:** `residuos`

**Campos:**

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT  
- `colegio_id`: INTEGER, NOT NULL, FOREIGN KEY → `colegios(id)`, ON DELETE CASCADE  
- `tipo`: VARCHAR(50), NOT NULL  
- `peso_kg`: FLOAT, NOT NULL  
- `volumen_litros`: FLOAT, NOT NULL  
- `aula`: VARCHAR(50), NOT NULL  
- `estado`: VARCHAR(30), NOT NULL  
- `fecha_registro`: DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP  

---

## 3. Tabla: alertas

**Nombre de la tabla:** `alertas`

**Campos:**

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT  
- `colegio_id`: INTEGER, NOT NULL, FOREIGN KEY → `colegios(id)`, ON DELETE CASCADE  
- `tipo_residuo`: VARCHAR(50), NOT NULL  
- `umbral_volumen`: FLOAT, NOT NULL  
- `activa`: BOOLEAN, NOT NULL, DEFAULT FALSE  
- `fecha_creacion`: DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP  

---

## Valores Controlados

**Tipo de residuo (residuos y alertas):**

- plastico  
- papel  
- vidrio  
- organico  
- electronico  

**Estado de residuo (residuos):**

- pendiente  
- reciclado  
