import json
import os
from datetime import date, datetime

DB_FILE = "datos_guerrero.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
                datos.setdefault('fallos', 3)
                datos.setdefault('racha', 0)
                datos.setdefault('historial', {})
                
                hoy = date.today()
                hoy_str = str(hoy)
                
                # Motor Dinámico de Misiones y Sirenas
                if datos.get('fecha_misiones') != hoy_str:
                    datos['misiones_hoy'] = [
                        {"tarea": "Despertar temprano y enfoque", "completada": False},
                        {"tarea": "Lectura / Desarrollo", "completada": False},
                        {"tarea": "Entrenamiento físico", "completada": False}
                    ]
                    datos['canto_sirenas'] = None # None = No respondido, True = Caí, False = Resistí
                    datos['fecha_misiones'] = hoy_str
                    datos['jornada_cerrada'] = False
                
                # Auditoría de Inactividad (El castigo por desaparecer)
                if 'ultima_actualizacion' in datos:
                    ultima_fecha = datetime.strptime(datos['ultima_actualizacion'], "%Y-%m-%d").date()
                    diferencia_dias = (hoy - ultima_fecha).days
                    
                    if hoy.month != ultima_fecha.month:
                        nombre_mes_anterior = ultima_fecha.strftime("%Y-%m")
                        datos['historial'][nombre_mes_anterior] = datos.get('fallos', 3)
                    
                    if diferencia_dias > 1:
                        # Si desapareces, te castiga por los días perdidos (Misiones + Sirenas evadidas)
                        dias_perdidos = diferencia_dias - 1
                        castigo_total = dias_perdidos * 2 # 1 por tareas, 1 por evadir sirenas
                        datos['fallos'] = min(7, datos['fallos'] + castigo_total)
                        datos['racha'] = 0
                        
                    if diferencia_dias > 0:
                         datos['ultima_actualizacion'] = hoy_str
                         guardar_datos(datos)
                else:
                    datos['ultima_actualizacion'] = hoy_str
                    
                return datos
        except:
            return {}
    return {}

def guardar_datos(datos):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def agregar_mision(nueva_tarea):
    """Permite al usuario inyectar nuevas tareas al día."""
    datos = cargar_datos()
    if not datos.get('jornada_cerrada', False):
        datos['misiones_hoy'].append({"tarea": nueva_tarea, "completada": False})
        guardar_datos(datos)

def guardar_estado_parcial(lista_estados, estado_sirenas):
    """Guarda el progreso de los checkboxes y las sirenas sin evaluar."""
    datos = cargar_datos()
    for i, estado in enumerate(lista_estados):
        datos['misiones_hoy'][i]['completada'] = estado
    datos['canto_sirenas'] = estado_sirenas
    guardar_datos(datos)

def evaluar_jornada():
    """Cierre del día: Calcula la disciplina total."""
    datos = cargar_datos()
    if datos.get('jornada_cerrada', False):
        return
    
    total_tareas = len(datos['misiones_hoy'])
    tareas_completadas = sum([1 for m in datos['misiones_hoy'] if m['completada']])
    sirenas = datos['canto_sirenas']
    
    fallos_actuales = datos.get('fallos', 3)
    racha_actual = datos.get('racha', 0)
    nuevos_strikes = 0

    # 1. Evaluación de Tareas
    if tareas_completadas < total_tareas:
        nuevos_strikes += 1

    # 2. Evaluación de Dopamina (Sirenas)
    if sirenas is None:
        nuevos_strikes += 1 # Castigo por evadir la pregunta
    elif sirenas == True:
        nuevos_strikes += 1 # Castigo por caer en el vicio

    # 3. Veredicto Final
    if nuevos_strikes == 0:
        # Victoria Absoluta
        datos['fallos'] = max(0, fallos_actuales - 1)
        datos['racha'] = racha_actual + 1
    else:
        # Derrota (Total o Parcial)
        datos['fallos'] = min(7, fallos_actuales + nuevos_strikes)
        datos['racha'] = 0

    datos['jornada_cerrada'] = True
    datos['ultima_actualizacion'] = str(date.today())
    guardar_datos(datos)