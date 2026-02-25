import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime
import pandas as pd
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
st.set_page_config(page_title="THE DROP: 15 SALVADOR", page_icon="🌴", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00f2ff; text-align: center; text-shadow: 0 0 10px #00f2ff; }
    .stAlert { background-color: #161b22; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("THE DROP: 15 // SALVADOR")
st.write("<h3 style='text-align: center; color: white;'>25 DE ABRIL | 4:00 PM - 4:00 AM</h3>", unsafe_allow_html=True)

# 2. CARGA DE IMÁGENES (JPEG)
col1, col2 = st.columns(2)
try:
    with col1:
        img1 = Image.open("salvador.jpeg")
        st.image(img1, caption="SALVADOR", use_container_width=True)
    with col2:
        img2 = Image.open("piscina.jpeg")
        st.image(img2, caption="LA LOCACIÓN", use_container_width=True)
except FileNotFoundError:
    st.error("Error: Asegúrate de tener 'salvador.jpeg' y 'piscina.jpeg' en la carpeta.")

# 3. LÓGICA DE TIEMPO (AUTODESTRUCCIÓN)
# Fecha de la fiesta: 25 de Abril, 2026 a las 16:00
fecha_evento = datetime.datetime(2026, 4, 25, 16, 0, 0)
ahora = datetime.datetime.now()
diferencia = fecha_evento - ahora

# 4. CONEXIÓN A GOOGLE SHEETS
# Debes crear un "Google Sheet" y obtener su URL pública
conn = st.connection("gsheets", type=GSheetsConnection)

if ahora < fecha_evento:
    st.info(f"⏳ EL SISTEMA SE AUTODESTRUIRÁ EN: {diferencia.days} días, {diferencia.seconds//3600} horas.")
    
    # Formulario de Registro
    with st.form(key="invitacion_form"):
        nombre = st.text_input("NOMBRE COMPLETO DEL INVITADO:")
        cancion = st.text_input("CANCIÓN INDISPENSABLE PARA LA POOL PARTY:")
        dieta = st.selectbox("RESTRICCIONES ALIMENTICIAS:", ["Ninguna", "Vegetariano", "Alérgico (especificar en nombre)", "Otro"])
        
        submit_button = st.form_submit_button(label="RECLAMAR MI PASE VIP")

        if submit_button:
            if nombre:
                # Leer datos actuales
                data = conn.read(worksheet="Invitados")
                
                # Crear nueva fila
                new_data = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre,
                    "Cancion": cancion,
                    "Dieta": dieta
                }])
                
                # Actualizar Google Sheets
                updated_df = pd.concat([data, new_data], ignore_index=True)
                conn.update(worksheet="Invitados", data=updated_df)
                
                st.balloons()
                st.success(f"¡CONFIRMADO! {nombre}, tu acceso VIP ha sido validado. Nos vemos el 25.")
            else:
                st.warning("El nombre es obligatorio para el acceso.")
else:
    # EFECTO DE AUTODESTRUCCIÓN
    st.error("🚨 ACCESO DENEGADO: EL SISTEMA SE HA AUTODESTRUIDO.")
    st.write("El registro para THE DROP: 15 ha finalizado. La base de datos ha sido sellada.")