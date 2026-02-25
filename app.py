import streamlit as st
import base64

# Configuración de la página
st.set_page_config(page_title="Salvador: THE DROP", layout="wide")

# Función para cargar el video localmente desde la carpeta static
def render_video(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    return f"""
        <video autoplay muted loop playsinline class="video-bg">
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
        </video>
    """

# Estilos CSS
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .video-bg {
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        object-fit: cover;
    }
    .main-content {
        position: relative;
        z-index: 1;
        text-align: center;
        color: white;
        padding-top: 20vh;
        font-family: 'Arial Black', sans-serif;
    }
    .neon-text {
        font-size: 5rem;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Renderizar el video y el contenido
try:
    # Usamos la ruta a la carpeta static que ya creaste
    video_html = render_video("static/invitacion_neon.mp4")
    st.markdown(video_html, unsafe_allow_html=True)
except:
    st.error("No se pudo cargar el video. Verifica que esté en static/invitacion_neon.mp4")

st.markdown(
    """
    <div class="main-content">
        <h1 class="neon-text">SALVADOR</h1>
        <p style="font-size: 2rem;">THE DROP: 15 AÑOS</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Botón de confirmación
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("CONFIRMAR ASISTENCIA", use_container_width=True):
        st.balloons()