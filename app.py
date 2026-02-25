import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Salvador: The Drop", layout="wide")

# URL directa de tu video en GitHub (Esta es la clave)
VIDEO_URL = "https://raw.githubusercontent.com/anhelloco-cpu/PoolParty-Salvador/main/static/invitacion_neon.mp4"

st.markdown(
    f"""
    <style>
    /* Ocultar elementos de Streamlit */
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
        font-size: 5rem;
        font-weight: bold;
        color: #fff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #ff00ff;
    }}
    </style>

    <video autoplay muted loop playsinline class="video-bg">
        <source src="{VIDEO_URL}" type="video/mp4">
        Tu navegador no soporta video.
    </video>

    <div class="main-content">
        <h1 class="neon-text">SALVADOR</h1>
        <p style="font-size: 2rem; text-shadow: 2px 2px 4px #000;">THE DROP: 15 AÑOS</p>
        <p style="font-size: 1.5rem;">25 DE ABRIL | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Botón de confirmación
st.write("<br>" * 5, unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("CONFIRMAR ASISTENCIA", use_container_width=True):
        st.balloons()
        st.success("¡Nos vemos en la pool party!")