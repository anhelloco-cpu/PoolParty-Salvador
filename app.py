import streamlit as st
import datetime
import time

# Configuración de la página
st.set_page_config(page_title="THE DROP: 15 SALVADOR", page_icon="🌴", layout="centered")

# Estilo CSS para que se vea Neón y tipo Festival
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stHeading h1 { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; font-family: 'Courier New', Courier, monospace; }
    .stText { color: #ffffff; }
    .stButton>button { 
        background-color: #ff00ff; 
        color: white; 
        border-radius: 20px; 
        border: none;
        box-shadow: 0 0 15px #ff00ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("THE DROP: 15 // SALVADOR")
st.subheader("COORDENADAS: 25 DE ABRIL | 4:00 PM - 4:00 AM")

# --- LÓGICA DEL CRONÓMETRO ---
# Definimos la fecha de la fiesta (o la fecha límite de registro)
fecha_fiesta = datetime.datetime(2026, 4, 25, 16, 0, 0)
ahora = datetime.datetime.now()
tiempo_restante = fecha_fiesta - ahora

if tiempo_restante.total_seconds() > 0:
    st.info(f"⚠️ EL SISTEMA SE AUTODESTRUIRÁ EN: {tiempo_restante.days} días, {tiempo_restante.seconds//3600} horas.")
    
    # Formulario de Registro
    with st.form("registro_vip"):
        st.write("### RECLAMA TU ACCESO VIP")
        nombre = st.text_input("NOMBRE DEL INVITADO")
        cancion = st.text_input("TRACK PARA EL AGUA (TU CANCIÓN)")
        confirmar = st.form_submit_button("CONFIRMAR ASISTENCIA")
        
        if confirmar:
            if nombre:
                st.success(f"¡REGISTRO EXITOSO! Bienvenido a la lista, {nombre}. Guarda tu pase.")
                # Aquí conectaríamos con Google Sheets después
            else:
                st.error("Debes ingresar tu nombre para validar el acceso.")
else:
    # --- LA AUTODESTRUCCIÓN ---
    st.error("🚨 ACCESO DENEGADO: EL SISTEMA SE HA AUTODESTRUIDO.")
    st.write("Los cupos para THE DROP: 15 se han agotado o el tiempo límite expiró.")