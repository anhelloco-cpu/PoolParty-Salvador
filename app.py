import streamlit as st
import pandas as pd
import datetime
from PIL import Image
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="THE DROP: 15 // SALVADOR", page_icon="🌴", layout="centered")

# Estilo CSS para la estética Neon/Dark
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1 { color: #00f2ff; text-align: center; text-shadow: 0 0 15px #00f2ff; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { 
        width: 100%; 
        background-color: #ff00ff; 
        color: white; 
        border-radius: 20px; 
        border: none;
        box-shadow: 0 0 10px #ff00ff;
    }
    .stButton>button:hover { background-color: #00f2ff; box-shadow: 0 0 20px #00f2ff; color: black; }
    </style>
    """, unsafe_allow_html=True)

# 2. MANEJO DE ESTADO (NAVEGACIÓN)
if 'paso' not in st.session_state:
    st.session_state.paso = 'invitacion'

# 3. CONEXIÓN A GOOGLE SHEETS
# Asegúrate de tener configurado el secreto en Streamlit Cloud
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Error de conexión. Verifica los Secrets en Streamlit.")

# --- FASE 1: LA INVITACIÓN ---
if st.session_state.paso == 'invitacion':
    st.write("<h1>THE DROP: 15</h1>")
    
    # Imagen principal (La que diseñamos con fondo de agua)
    try:
        st.image("invitacion_final.jpeg", use_container_width=True)
    except:
        st.info("Sube 'invitacion_final.jpeg' a tu repositorio de GitHub.")

    # Cronómetro dinámico
    fecha_evento = datetime.datetime(2026, 4, 25, 16, 0, 0) #
    ahora = datetime.datetime.now()
    diferencia = fecha_evento - ahora

    if ahora < fecha_evento:
        col1, col2, col3 = st.columns(3)
        col1.metric("Días", diferencia.days)
        col2.metric("Horas", diferencia.seconds // 3600)
        col3.metric("Minutos", (diferencia.seconds // 60) % 60)
        
        st.write("---")
        if st.button("ACEPTAR INVITACIÓN Y REGISTRARME"):
            st.session_state.paso = 'formulario'
            st.rerun()
    else:
        st.error("EL SISTEMA SE HA AUTODESTRUIDO. EL REGISTRO ESTÁ CERRADO.")

# --- FASE 2: EL FORMULARIO ---
elif st.session_state.paso == 'formulario':
    st.write("<h1>REGISTRO VIP</h1>")
    st.write("Completa tus datos para asegurar tu brazalete de acceso.")

    with st.form("registro_form"):
        nombre = st.text_input("Nombre Completo:")
        cancion = st.text_input("¿Qué canción quieres escuchar en la pool party?")
        dieta = st.selectbox("Restricciones Alimenticias:", ["Ninguna", "Vegetariano", "Alérgico", "Otro"])
        
        enviar = st.form_submit_button("CONFIRMAR ASISTENCIA")

        if enviar:
            if nombre:
                # Crear DataFrame con el nuevo invitado
                nuevo_invitado = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nombre": nombre,
                    "Cancion": cancion,
                    "Dieta": dieta
                }])
                
                try:
                    # Leer datos existentes y actualizar
                    df_actual = conn.read(worksheet="Sheet1")
                    df_final = pd.concat([df_actual, nuevo_invitado], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=df_final)
                    
                    st.balloons()
                    st.success(f"¡Todo listo, {nombre}! Tu cupo está asegurado.")
                    if st.button("Volver al inicio"):
                        st.session_state.paso = 'invitacion'
                        st.rerun()
                except Exception as e:
                    st.error("Hubo un problema al guardar tus datos. Intenta más tarde.")
            else:
                st.warning("Por favor, ingresa tu nombre.")