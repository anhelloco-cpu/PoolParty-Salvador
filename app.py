import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="The Drop: Salvador 15", layout="wide")

# 2. URL de tu video (esta ruta apunta directo a tu archivo en GitHub)
VIDEO_URL = "https://raw.githubusercontent.com/anhelloco-cpu/PoolParty-Salvador/main/static/invitacion_neon.mp4"

# 3. Estilos y Video
st.markdown(
    f"""
    <style>
    #MainMenu, footer, header {{visibility: hidden;}}
    .video-bg {{
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        object-fit: cover;
    }}
    .content {{
        position: relative;
        z-index: 1;
        text-align: center;
        color: white;
        padding-top: 20vh;
        font-family: 'Arial Black', sans-serif;
    }}
    .neon {{
        font-size: 5rem;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
    }}
    </style>
    
    <video autoplay muted loop playsinline class="video-bg">
        <source src="{VIDEO_URL}" type="video/mp4">
    </video>

    <div class="content">
        <h1 class="neon">SALVADOR</h1>
        <p style="font-size: 2rem;">THE DROP: 25 DE ABRIL</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Botón de confirmación
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("CONFIRMAR ASISTENCIA", use_container_width=True):
        st.balloons()
        st.success("¡Confirmado!")