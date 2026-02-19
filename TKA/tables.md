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
- `categoria_id`: INTEGER, NOT NULL, FOREIGN KEY → `categorias(id)`
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
- `categoria_id`: INTEGER, NOT NULL, FOREIGN KEY → `categorias(id)`
- `umbral_volumen`: FLOAT, NOT NULL  
- `activa`: BOOLEAN, NOT NULL, DEFAULT FALSE  
- `fecha_creacion`: DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP  

---

## 4. Tabla: categorias

**Nombre de la tabla:** `categorias`

**Campos:**

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `code`: VARCHAR(50), NOT NULL, UNIQUE (Ej: "ORGANIC")
- `label`: VARCHAR(100), NOT NULL
- `umbral`: INTEGER, NOT NULL (Default: 100)
- `icon`: VARCHAR(50), NOT NULL
- `color`: VARCHAR(50), NOT NULL
- `bg`: VARCHAR(50), NOT NULL
- `fecha_creacion`: DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP

---

## Valores Controlados Actualizados

**Categorías Estándar (Seed inicial):**

1. **ORGANIC (Orgánico):** 🥬 / #f59e0b
2. **PLASTIC (Plástico):** ♻️ / #2ecc71
3. **PAPER (Papel):** 📄 / #3b82f6
4. **GLASS (Vidrio):** 🪟 / #06b6d4
5. **WASTE (Residuos):** 🗑️ / #8b5cf6
6. **HAZARD (Peligroso):** ⚠️ / #ef4444
