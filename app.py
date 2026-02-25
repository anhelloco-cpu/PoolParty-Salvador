import streamlit as st
import datetime
from streamlit_gsheets import GSheetsConnection

# Estética Neon
st.set_page_config(page_title="THE DROP: 15", layout="centered")

# Control de navegación
if 'paso' not in st.session_state:
    st.session_state.paso = 'invitacion'

# --- PASO 1: LA INVITACIÓN ---
if st.session_state.paso == 'invitacion':
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>THE DROP: 15</h1>", unsafe_allow_html=True)
    
    # Aquí cargamos la imagen que diseñamos
    st.image("invitacion_final.jpeg", use_container_width=True)
    
    if st.button("ACEPTAR INVITACIÓN"):
        st.session_state.paso = 'formulario'
        st.rerun()

# --- PASO 2: EL REGISTRO ---
elif st.session_state.paso == 'formulario':
    st.header("REGISTRO VIP")
    with st.form("registro"):
        nombre = st.text_input("Nombre completo:")
        cancion = st.text_input("Tu canción para la fiesta:")
        if st.form_submit_button("CONFIRMAR"):
            # Aquí va la lógica de Google Sheets que ya configuramos
            st.balloons()
            st.success("¡Nos vemos el 25 de abril!")