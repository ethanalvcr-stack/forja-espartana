import streamlit as st
import datetime
from utils.db_handler import cargar_datos, guardar_datos

st.set_page_config(page_title="Diagnóstico", page_icon="🧠", layout="wide")

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
        .stButton>button { border: 1px solid #D4AF37; color: #D4AF37; background-color: #0a0a0a; font-weight: bold; border-radius: 8px; transition: 0.3s; }
        .stButton>button:hover { background-color: #D4AF37; color: #0a0a0a; border: 1px solid #D4AF37; }
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { border-color: #333333 !important; background-color: #111111 !important; }
    </style>
""", unsafe_allow_html=True)

datos = cargar_datos()

if datos:
    st.success(f"🛡️ Guerrero registrado: **{datos.get('nombre_batalla', 'Héroe')}**. El perfil ya está forjado.")
else:
    st.title("📜 Auditoría Inicial de Identidad")
    
    with st.form("form_diagnostico"):
        st.subheader("I. Identidad del Guerrero")
        nombre_batalla = st.text_input("Tu Nombre de Batalla / Identificador", placeholder="Ej. Ethan, Leónidas, Valquiria...")

        st.markdown("---")
        st.subheader("II. Fisiología y Biomecánica")
        col1, col2, col3 = st.columns(3)
        with col1: genero = st.selectbox("Género Biológico", ["Masculino", "Femenino"])
        with col2: edad = st.number_input("Edad", min_value=12, max_value=100, value=21)
        with col3: peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=75.0)
            
        lesiones = st.text_area("Historial de Lesiones", placeholder="Ej. Molestia en rodilla derecha...")

        st.markdown("---")
        st.subheader("III. Mente y Entorno")
        estado_sentimental = st.selectbox("Estado Sentimental", ["Soltero/a", "En relación estable", "Proceso de recuperación/duelo (Ruptura reciente)"])
        
        st.markdown("### Control de Fugas de Energía")
        frecuencia_fugas = st.slider("Frecuencia semanal en la que cedes a fugas (dopamina barata)", 0, 7, 3)

        if st.form_submit_button("Forjar Perfil"):
            if not nombre_batalla.strip():
                nombre_batalla = "Guerrero Anónimo"
                
            nivel_asignado = 1 if (frecuencia_fugas > 3 or estado_sentimental == "Proceso de recuperación/duelo (Ruptura reciente)") else 2
            
            perfil = {
                "nombre_batalla": nombre_batalla,
                "genero": genero,
                "edad": edad,
                "peso": peso,
                "lesiones": lesiones,
                "estado_sentimental": estado_sentimental,
                "frecuencia_fugas": frecuencia_fugas,
                "fecha_registro": str(datetime.date.today()),
                "nivel_base_asignado": nivel_asignado
            }
            guardar_datos(perfil)
            st.success("¡Perfil generado con éxito!")
            st.balloons()