import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="THE DROP: 15 SALVADOR", page_icon="🌴", layout="centered")

# ESTILO CSS PARA EFECTO "TARJETA NEÓN"
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at bottom, #1a0b2e 0%, #0e1117 100%);
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2.5rem;
        border-radius: 25px;
        border: 1px solid rgba(0, 242, 255, 0.4);
        box-shadow: 0 0 40px rgba(0, 242, 255, 0.2);
        backdrop-filter: blur(12px);
        text-align: center;
    }
    h1 { color: #00f2ff !important; text-shadow: 0 0 15px #00f2ff; font-family: 'Courier New'; }
    .stButton>button { 
        width: 100%;
        background: linear-gradient(90deg, #ff00ff, #00f2ff) !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        border: none !important;
        height: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# MANEJO DE NAVEGACIÓN
if 'paso' not in st.session_state:
    st.session_state.paso = 'invitacion'

# CONEXIÓN A GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# --- PASO 1: LA INVITACIÓN ---
if st.session_state.paso == 'invitacion':
    st.markdown("<h1>THE DROP: 15</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Asegúrate de subir la imagen de la invitación a GitHub con este nombre
        try:
            st.image("invitacion_neon.jpg", use_container_width=True)
        except:
            st.info("Sube 'invitacion_neon.jpg' a tu GitHub para ver el diseño.")
            
        st.write("### 25 DE ABRIL | 4:00 PM")
        if st.button("ACEPTAR INVITACIÓN (GET WRISTBAND)"):
            st.session_state.paso = 'registro'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 2: EL FORMULARIO ---
elif st.session_state.paso == 'registro':
    st.markdown("<h1>CONFIRMA TU ASISTENCIA</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("registro_vip"):
            nombre = st.text_input("NOMBRE COMPLETO")
            cancion = st.text_input("TU CANCIÓN PARA LA POOL PARTY")
            dieta = st.selectbox("DIETA / ALERGIAS", ["Sin restricciones", "Vegetariano", "Alérgico", "Otro"])
            
            submit = st.form_submit_button("REGISTRARME AHORA")
            
            if submit:
                if nombre:
                    # Crear nueva fila
                    nueva_fila = pd.DataFrame([{
                        "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Nombre": nombre,
                        "Cancion": cancion,
                        "Dieta": dieta
                    }])
                    
                    # Leer y actualizar la hoja
                    df_actual = conn.read(worksheet="Sheet1")
                    df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=df_final)
                    
                    st.balloons()
                    st.success(f"¡Listo {nombre}! Nos vemos en la fiesta.")
                else:
                    st.error("Por favor, pon tu nombre.")
        
        if st.button("VOLVER A VER INVITACIÓN"):
            st.session_state.paso = 'invitacion'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)