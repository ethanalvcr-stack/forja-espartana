import streamlit as st
import datetime
from utils.db_handler import cargar_datos, actualizar_progreso

st.set_page_config(page_title="Misiones", page_icon="⚔️", layout="centered")

st.markdown("""
    <style>
        .stApp { 
            background-color: #0a0a0a;
            background-image: 
                linear-gradient(45deg, #141414 25%, transparent 25%, transparent 75%, #141414 75%, #141414),
                linear-gradient(45deg, #141414 25%, transparent 25%, transparent 75%, #141414 75%, #141414);
            background-size: 4px 4px;
            background-position: 0 0, 2px 2px;
            color: #fafafa; 
        }
        h1, h2, h3 { color: #D4AF37 !important; font-family: 'Georgia', serif !important; text-transform: uppercase; letter-spacing: 2px; }
        .stButton>button { border: 1px solid #D4AF37; color: #D4AF37; background-color: #0a0a0a; font-weight: bold; border-radius: 8px; width: 100%; transition: 0.3s; }
        .stButton>button:hover { background-color: #D4AF37; color: #0a0a0a; }
        .mission-box { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background-color: rgba(17, 17, 17, 0.8); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ BITÁCORA DEL HÉROE")
st.subheader(f"DIARIO: {datetime.date.today()}")

st.write("---")
st.title("⚔️ PRUEBAS DEL DIA")

# Creamos las pruebas de disciplina
mision_1 = st.checkbox("Hábito de la mañana 1 (Despertar temprano y enfoque)")
st.caption("🕒 06:00")

mision_2 = st.checkbox("Hábito de la mañana 2 (Lectura / Desarrollo)")
st.caption("🕒 07:00")

mision_3 = st.checkbox("Entrenamiento físico del día (Protocolo de fuerza)")
st.caption("🕒 18:00")

st.write("")

if st.button("REPORTAR AVANCE DE HOY"):
    total_completadas = sum([mision_1, mision_2, mision_3])
    actualizar_progreso(total_completadas, 3)
    
    if total_completadas == 3:
        st.success("🔥 ¡Misiones cumplidas con éxito! Recompensa aplicada: Menos un strike, racha incrementada.")
    else:
        st.warning(f"⚠️ Has completado {total_completadas}/3 misiones. La disciplina incompleta ajusta tus strikes.")
    
    st.rerun()