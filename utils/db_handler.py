import json
import os

DB_FILE = "datos_guerrero.json"

def cargar_datos():
    """Carga los datos del usuario si el archivo existe."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_datos(datos):
    """Guarda los datos del usuario en el archivo local."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)