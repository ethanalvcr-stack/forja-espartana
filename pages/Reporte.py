import streamlit as st
from utils.db_handler import cargar_datos
from utils.avatar_logic import obtener_ruta_avatar, calcular_nivel_actual

st.set_page_config(page_title="Informe Mensual", page_icon="📊", layout="wide")

# --- DISEÑO ---
st.markdown("""
    <style>
        .stApp { 
            background-color: #0a0a0a;
            background-image: linear-gradient(45deg, #141414 25%, transparent 25%, transparent 75%, #141414 75%, #141414),
                              linear-gradient(45deg, #141414 25%, transparent 25%, transparent 75%, #141414 75%, #141414);
            background-size: 4px 4px; background-position: 0 0, 2px 2px; color: #fafafa; 
        }
        h1, h2 { color: #D4AF37 !important; font-family: 'Georgia', serif !important; text-transform: uppercase; letter-spacing: 2px; }
        .stat-box { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background-color: #111; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 ARCHIVOS DE GUERRA: TU PROGRESO")
datos = cargar_datos()

if not datos:
    st.warning("Aún no hay datos para generar el informe.")
else:
    # Obtenemos tu estado actual para proyectarlo en el informe
    # En el futuro, aquí leeremos un histórico de fechas
    nivel_actual = calcular_nivel_actual(3) # Asumimos 3 fallos (tu nivel actual de inicio)
    genero = datos.get('genero', 'Masculino')
    ruta_avatar = obtener_ruta_avatar(genero, nivel_actual)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Estatus Actual")
        st.image(ruta_avatar, use_container_width=True)
        st.markdown(f"**Nivel de Disciplina:** {nivel_actual}")

    with col2:
        st.markdown("### Resumen de Campaña")
        st.write("Visualiza aquí cómo tu nivel ha oscilado semanalmente.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="stat-box"><h3>Semanal</h3><p>Nivel 0</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="stat-box"><h3>Mensual</h3><p>En proceso...</p></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.metric(label="Racha Actual (Días sin fallar)", value="0", delta="0")