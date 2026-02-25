import streamlit as st
import base64
import os

# 1. Configuración de página
st.set_page_config(page_title="The Drop: Salvador 15", layout="wide")

# 2. Función para cargar el video de forma segura
def get_video_html(video_path):
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        video_base64 = base64.b64encode(video_bytes).decode()
        return f"""
            <video autoplay muted loop playsinline class="video-bg">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        """
    return ""

# 3. Aplicar CSS y mostrar el Video
video_html = get_video_html("invitacion_neon.mp4")

st.markdown(
    f"""
    <style>
    #MainMenu, footer, header {{visibility: hidden;}}
    
    .video-bg {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1;
        object-fit: cover;
    }}

    .main-content {{
        position: relative;
        z-index: 1;
        text-align: center;
        color: white;
        padding-top: 15vh;
        font-family: 'Arial Black', sans-serif;
    }}

    .neon-text {{
        font-size: clamp(2rem, 8vw, 5rem);
        font-weight: bold;
        text-transform: uppercase;
        color: #fff;
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #0fa,
            0 0 82px #0fa,
            0 0 92px #0fa;
    }}
    </style>

    {video_html}

    <div class="main-content">
        <h1 class="neon-text">SALVADOR: THE DROP</h1>
        <p style="font-size: 1.5rem; text-shadow: 2px 2px 4px #000;">25 DE ABRIL | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Botón de confirmación centrado
st.write("<br>" * 3, unsafe_allow_html=True) # Espaciador
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("CONFIRMAR ASISTENCIA", use_container_width=True):
        st.balloons()
        st.success("¡Nos vemos en la pool party, Salvador!")