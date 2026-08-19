import streamlit as st
import datetime

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
        div[data-baseweb="input"] > div { border-color: #333333 !important; background-color: #111111 !important; }
        .mission-box { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background-color: rgba(17, 17, 17, 0.8); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ BITÁCORA DEL HÉROE")
st.subheader(f"DIARIO: {datetime.date.today()}")

# Contenedor para la nueva misión
st.markdown('<div class="mission-box">', unsafe_allow_html=True)
st.write("¿Qué nueva misión surge hoy?")
nueva_mision = st.text_input("", placeholder="Ej. Entrenar fuerza 1 hr...", label_visibility="collapsed")
hora_limite = st.time_input("Hora límite", datetime.time(16, 8))
st.button("Aceptar Reto")
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.title("⚔️ PRUEBAS DEL DÍA")

st.checkbox("Hábito de la mañana 1 (Ej. Despertar temprano) ⚠️")
st.caption("🕒 06:00")
st.checkbox("Hábito de la mañana 2 (Ej. Leer 10 págs)")
st.caption("🕒 07:00")
st.checkbox("Entrenamiento físico del día (Protocolo de fuerza)")
st.caption("🕒 18:00")