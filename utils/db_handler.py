import json
import os
from datetime import date

DB_FILE = "datos_guerrero.json"

def cargar_datos():
    """Carga los datos del usuario o devuelve una estructura base por defecto."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                # Asegurar llaves base por si el JSON es antiguo
                if 'fallos' not in datos:
                    datos['fallos'] = 3
                if 'racha' not in datos:
                    datos['racha'] = 0
                return datos
        except:
            return {}
    return {}

def guardar_datos(datos):
    """Guarda todo el diccionario de datos en el archivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def actualizar_progreso(tareas_completadas, total_tareas=3):
    """Aplica la recompensa por completar misiones o evalúa el estatus."""
    datos = cargar_datos()
    if not datos:
        return
    
    hoy = str(date.today())
    ultimo_registro = datos.get('ultima_actualizacion', '')

    # Evitamos sumar/restar múltiples veces el mismo día si ya se reportó
    if ultimo_registro != hoy:
        fallos_actuales = datos.get('fallos', 3)
        racha_actual = datos.get('racha', 0)

        if tareas_completadas == total_tareas:
            # RECOMPENSA: Si completas todo, restas un fallo (mejoras tu nivel) y sube tu racha
            datos['fallos'] = max(0, fallos_actuales - 1)
            datos['racha'] = racha_actual + 1
        elif tareas_completadas < total_tareas:
            # CASTIGOS/FALTA DE DISCIPLINA: Si dejas tareas incompletas, aumenta un fallo
            datos['fallos'] = min(7, fallos_actuales + 1)
            datos['racha'] = 0 # Se rompe la racha si flaqueas

        datos['ultima_actualizacion'] = hoy
        guardar_datos(datos)
        