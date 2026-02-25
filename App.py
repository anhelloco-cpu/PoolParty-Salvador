import streamlit as st
import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="THE DROP: 15 SALVADOR", page_icon="🌴", layout="centered")

# --- ESTILO TIPO FESTIVAL (CSS) ---
st.markdown("""
    <style>
    /* Fondo y tipografía general */
    .main { background-color: #0e1117; color: white; }
    
    /* Efecto Neón para el Título */
    .neon-title {
        text-align: center;
        color: #fff;
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #00f2ff, 0 0 30px #00f2ff;
        font-family: 'Courier New', Courier, monospace;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0px;
    }

    /* Contenedor de la Imagen con Brillo */
    .img-container {
        border: 2px solid #ff00ff;
        box-shadow: 0 0 20px #ff00ff;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
    }

    /* Alerta de Autodestrucción */
    .destruct-msg {
        background-color: rgba(255, 0, 0, 0.2);
        border: 1px solid #ff0000;
        padding: 15px;
        border-radius: 10px;
        color: #ff4b4b;
        text-align: center;
        font-weight: bold;
        animation: blinker 1.5s linear infinite;
    }

    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown('<p class="neon-title">THE DROP: 15</p>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #00f2ff;'>SALVADOR</h2>", unsafe_allow_html=True)

# --- IMAGEN PRINCIPAL (Debes poner el link de la imagen que generamos) ---
# Si la tienes local, usa st.image("tu_imagen.png")
st.markdown('<div class="img-container">', unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1519750157634-b6d493a0f77c?q=80&w=1000&auto=format&fit=crop", caption="📍 COORDENADAS: 25 ABRIL | 4 PM - 4 AM") 
st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE AUTODESTRUCCIÓN ---
fecha_fiesta = datetime.datetime(2026, 4, 25, 16, 0)
ahora = datetime.datetime.now()

if ahora < fecha_fiesta:
    # SI EL TIEMPO NO HA EXPIRADO
    st.markdown(f'<div class="destruct-msg">⚠️ EL SISTEMA SE AUTODESTRUIRÁ EN: {(fecha_fiesta - ahora).days} DÍAS </div>', unsafe_allow_html=True)
    
    st.write("") # Espacio
    
    with st.form("registro_vip"):
        st.markdown("### 📥 RECLAMA TU PASE VIP")
        nombre = st.text_input("NOMBRE DEL AGENTE / INVITADO")
        cancion = st.text_input("TRACK PARA EL AGUA (TU CANCIÓN)")
        
        # Botón con estilo personalizado
        submit = st.form_submit_button("CONFIRMAR ASISTENCIA")
        
        if submit:
            if nombre:
                st.balloons()
                st.success(f"¡REGISTRO EXITOSO! {nombre}, estás en la lista. Prepárate para las 12 horas.")
                # Aquí es donde conectamos con tu Google Sheets
            else:
                st.warning("Escribe tu nombre para validar el acceso.")
else:
    # SI EL TIEMPO EXPIRÓ (AUTODESTRUCCIÓN)
    st.markdown("""
        <div style="text-align: center; padding: 50px; border: 5px solid red; border-radius: 20px;">
            <h1 style="color: red;">🚨 ACCESO DENEGADO 🚨</h1>
            <p style="font-size: 20px;">El sistema se ha autodestruido. <br> 
            Los cupos para THE DROP: 15 están cerrados.</p>
        </div>
    """, unsafe_allow_html=True)