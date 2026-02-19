## 1. Desactivar el entorno virtual
`deactivate`

## 2. Eliminar el entorno virtual
`rm -rf venv`

## 3. Crear un entorno virtual nuevo
`python3 -m venv venv`

## 4. Activar el entorno virtual
`source venv/bin/activate`

## 5. Reinstalar las dependencias
`pip install --force-reinstall -r requirements.txt`

## 6. Cerrar procesos bloqueados
`lsof -i :8000    # Para encontrar los procesos`
`kill -9 7883 8260 # Para cerrar los procesos bloqueados`

## 7. Ejecución
`source venv/bin/activate && uvicorn main:app --reload`

## 9. Solucionar Error 500 (Inconsistencia de Datos o Cache)
Si experimentas un `Internal Server Error` tras cambios de esquema:

1. **Detener el servidor**: `Ctrl+C` en la terminal.
2. **Borrar base de datos**: `rm residuos.db`
3. **Re-ejecutar Seed**: `./venv/bin/python3 seed.py`
4. **Reiniciar Servidor**: `./venv/bin/python3 -m uvicorn main:app --reload`