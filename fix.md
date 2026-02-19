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

## 8. Comprobación
`curl http://127.0.0.1:8000/`

## pruebas