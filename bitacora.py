import streamlit as st
import os
from utils.db_handler import cargar_datos
from utils.avatar_logic import obtener_ruta_avatar, calcular_nivel_actual

st.set_page_config(page_title="Cuartel General", page_icon="🏛️", layout="wide")

# --- DISEÑO DORADO Y TEXTURA VOLCÁNICA ---
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
    </style>
""", unsafe_allow_html=True)

# --- AJUSTES DE SISTEMA ---
with st.sidebar:
    st.markdown("### ⚙️ AJUSTES DE SISTEMA")
    if st.button("🗑️ Borrar Perfil y Reiniciar"):
        if os.path.exists("datos_guerrero.json"):
            os.remove("datos_guerrero.json")
            st.rerun()

datos = cargar_datos()

if not datos:
    st.title("⚔️ Cuartel General")
    st.warning("⚠️ Perfil de guerrero no detectado.")
    st.info("👉 Dirígete a la pestaña **Diagnóstico** para registrar tu identidad.")
else:
    nombre = datos.get('nombre_batalla', 'Guerrero')
    st.title(f"⚔️ Cuartel General: {nombre}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Iniciamos en 3 para que el guerrero empiece en Nivel 0
        fallos = st.number_input("Fallos (Strikes) esta semana", min_value=0, max_value=7, value=3)
        
        nivel_actual = calcular_nivel_actual(fallos)
        genero_usuario = datos.get('genero', 'Masculino')
        ruta_avatar = obtener_ruta_avatar(genero_usuario, nivel_actual)
        
        st.image(ruta_avatar, caption=f"Rango: Nivel {nivel_actual}", use_container_width=True)
        
        # Lógica de advertencia inteligente
        if 0 < nivel_actual < 2:
            st.error("🚨 ¡CUIDADO! Un fallo más y desciendes al Nivel 0.")
        elif nivel_actual == 0:
            st.warning("⚠️ Rango inicial: Disciplina requerida para ascender.")
            
    with col2:
        st.header("📜 TU MANDATO OPERATIVO")
        estado = datos.get('estado_sentimental', '')
        fugas = datos.get('frecuencia_fugas', 0)
        
        st.success("Estado de Identidad: Activo y en pie de lucha.")
        if fugas > 3:
            st.error("Control de dopamina inestable. ¡Refuerza el blindaje!")
        else:
            st.success("Control de dopamina estable. Mantén la guardia.")
            
        st.write("---")
        st.subheader("OBJETIVO DEL DÍA")
        st.write("Dirígete a la pestaña **Misiones** para reportar tus tareas.")