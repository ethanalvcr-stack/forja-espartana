import streamlit as st
import datetime
from utils.db_handler import cargar_datos, guardar_estado_parcial, evaluar_jornada, agregar_mision

st.set_page_config(page_title="Misiones", page_icon="⚔️", layout="centered")

st.markdown("""
    <style>
        .stApp { background-color: #0a0a0a; color: #fafafa; }
        h1, h2, h3 { color: #D4AF37 !important; font-family: 'Georgia', serif !important; text-transform: uppercase; letter-spacing: 2px; }
        .stButton>button { border: 1px solid #D4AF37; color: #D4AF37; background-color: #0a0a0a; font-weight: bold; border-radius: 8px; width: 100%; transition: 0.3s; }
        .stButton>button:hover { background-color: #D4AF37; color: #0a0a0a; }
        .sirenas-box { border: 2px solid #8b0000; padding: 15px; border-radius: 8px; background-color: rgba(139, 0, 0, 0.1); margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ BITÁCORA DEL HÉROE")
st.subheader(f"DIARIO: {datetime.date.today()}")

# 1. Cargar Memoria
datos = cargar_datos()
misiones = datos.get('misiones_hoy', [])
jornada_cerrada = datos.get('jornada_cerrada', False)
estado_sirenas_db = datos.get('canto_sirenas', None)

# 2. Agregar Nuevas Tareas (Solo si la jornada está abierta)
if not jornada_cerrada:
    with st.expander("➕ Agregar Nueva Misión"):
        nueva_tarea = st.text_input("Define tu nueva tarea:")
        if st.button("Añadir a la lista"):
            if nueva_tarea:
                agregar_mision(nueva_tarea)
                st.rerun()

st.write("---")
st.title("⚔️ PRUEBAS DEL DÍA")

# 3. Renderizar Checkboxes Dinámicamente
estados_checkboxes = []
for i, mision in enumerate(misiones):
    estado = st.checkbox(mision['tarea'], value=mision['completada'], disabled=jornada_cerrada, key=f"mision_{i}")
    estados_checkboxes.append(estado)

# 4. El Interrogatorio de las Sirenas
st.markdown('<div class="sirenas-box">', unsafe_allow_html=True)
st.markdown("### 🧜‍♀️ EL CANTO DE LAS SIRENAS")
st.write("¿Caíste ante la dopamina barata hoy? (Vicios, distracciones extremas, falta de control)")

opciones_sirenas = ["(No respondido)", "No, mantuve la disciplina", "Sí, cedí al vicio"]
# Mapear el valor de la DB a la opción del Selectbox
index_actual = 0
if estado_sirenas_db is False: index_actual = 1
elif estado_sirenas_db is True: index_actual = 2

seleccion_sirenas = st.radio("Confiesa:", opciones_sirenas, index=index_actual, disabled=jornada_cerrada)

# Traducir la selección a booleano
estado_sirenas_actual = None
if seleccion_sirenas == "No, mantuve la disciplina": estado_sirenas_actual = False
elif seleccion_sirenas == "Sí, cedí al vicio": estado_sirenas_actual = True
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# 5. Botones de Acción
if not jornada_cerrada:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 GUARDAR AVANCE"):
            guardar_estado_parcial(estados_checkboxes, estado_sirenas_actual)
            st.success("¡Avance reportado en la memoria!")
    with col2:
        if st.button("⚖️ CERRAR JORNADA"):
            # Último guardado antes de evaluar
            guardar_estado_parcial(estados_checkboxes, estado_sirenas_actual)
            evaluar_jornada()
            st.rerun()
else:
    st.info("⚔️ La jornada ha sido evaluada. El veredicto está en tus Archivos de Guerra.")