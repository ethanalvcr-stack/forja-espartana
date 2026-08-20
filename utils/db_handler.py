import json
import os
from datetime import date, datetime

DB_FILE = "datos_guerrero.json"

def cargar_datos():
    """Carga los datos y audita inactividad o cambios de mes automáticamente."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
                # 1. Asegurar estructura base
                datos.setdefault('fallos', 3)
                datos.setdefault('racha', 0)
                datos.setdefault('historial', {})
                
                # 2. El Guardián del Tiempo (Auditoría de disciplina)
                hoy = date.today()
                if 'ultima_actualizacion' in datos:
                    ultima_fecha = datetime.strptime(datos['ultima_actualizacion'], "%Y-%m-%d").date()
                    diferencia_dias = (hoy - ultima_fecha).days
                    
                    # A. Cambio de mes: Guardar la "foto" de cómo terminaste
                    if hoy.month != ultima_fecha.month:
                        nombre_mes_anterior = ultima_fecha.strftime("%Y-%m")
                        datos['historial'][nombre_mes_anterior] = datos.get('fallos', 3)
                    
                    # B. Castigo por inactividad (No abrir la app)
                    if diferencia_dias > 1:
                        dias_perdidos = diferencia_dias - 1
                        datos['fallos'] = min(7, datos['fallos'] + dias_perdidos)
                        datos['racha'] = 0
                        
                    # Auto-guardar si hubo castigos o cambios de mes por inactividad
                    if diferencia_dias > 0:
                         datos['ultima_actualizacion'] = str(hoy)
                         guardar_datos(datos)
                else:
                    datos['ultima_actualizacion'] = str(hoy)
                    
                return datos
        except:
            return {}
    return {}

def guardar_datos(datos):
    """Guarda todo el diccionario de datos en el archivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def actualizar_progreso(tareas_completadas, total_tareas=3):
    """Aplica la recompensa del día actual."""
    datos = cargar_datos()
    if not datos:
        return
    
    hoy = str(date.today())
    fallos_actuales = datos.get('fallos', 3)
    racha_actual = datos.get('racha', 0)

    if tareas_completadas == total_tareas:
        datos['fallos'] = max(0, fallos_actuales - 1)
        datos['racha'] = racha_actual + 1
    else:
        datos['fallos'] = min(7, fallos_actuales + 1)
        datos['racha'] = 0

    datos['ultima_actualizacion'] = hoy
    guardar_datos(datos)