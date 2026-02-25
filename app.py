import streamlit as st

# 1. Configuración de página (Debe ser lo primero)
st.set_page_config(page_title="The Drop: Salvador 15", layout="wide")

# 2. Estilo CSS para el fondo y limpiar la interfaz de Streamlit
st.markdown(
    """
    <style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor del video de fondo */
    .video-bg {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1;
    }

    /* Capa de contenido */
    .main-content {
        position: relative;
        z-index: 1;
        text-align: center;
        color: white;
        margin-top: 15vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .neon-text {
        font-size: 50px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. HTML para el Video (Carga directa sin Base64 para mayor velocidad)
# Nota: El archivo debe estar en la misma carpeta que app.py
st.markdown(
    """
    <video autoplay muted loop playsinline class="video-bg">
        <source src="https://raw.githubusercontent.com/tu-usuario/tu-repo/main/invitacion_neon.mp4" type="video/mp4">
        <source src="static/invitacion_neon.mp4" type="video/mp4">
    </video>

    <div class="main-content">
        <h1 class="neon-text">SALVADOR: THE DROP</h1>
        <p style="font-size: 20px;">25 de Abril | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Botón de confirmación (opcional)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("CONFIRMAR ASISTENCIA"):
        st.balloons()
        st.success("¡Registrado! Nos vemos en la piscina.")