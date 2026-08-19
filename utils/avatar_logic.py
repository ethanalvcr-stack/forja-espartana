def obtener_ruta_avatar(genero, nivel):
    """Devuelve la ruta correcta de la imagen según el género y el nivel."""
    suffix = "_fem" if genero == "Femenino" else ""
    return f"images/nivel{nivel}{suffix}.png"

def calcular_nivel_actual(fallos_semana):
    """
    Progresión RPG estricta:
    - Si tienes 3 o más fallos: Nivel 0 (Castigo / Recluta)
    - Si tienes 2 fallos: Nivel 1 
    - Si tienes 1 fallo: Nivel 2
    - Si tienes 0 fallos: Nivel 3 (Solo para los que mantienen el templo impecable)
    
    *Nota: Para que un usuario nuevo empiece en Nivel 0 por defecto, 
    asegúrate de que su contador inicial refleje una auditoría pendiente o empiece en Nivel 0.*
    """
    if fallos_semana >= 3:
        return 0  
    elif fallos_semana == 2:
        return 1  
    elif fallos_semana == 1:
        return 2  
    else:
        return 3