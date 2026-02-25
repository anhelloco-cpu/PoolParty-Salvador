import streamlit as st

# 1. Configuración de la página
st.set_page_config(page_title="Salvador: THE DROP", layout="wide")

# 2. Ruta directa de GitHub (Esto evita problemas de carpetas locales)
# Esta URL apunta directamente al archivo que acabas de subir
VIDEO_URL = "https://raw.githubusercontent.com/anhelloco-cpu/PoolParty-Salvador/main/static/invitacion_neon.mp4"

# 3. Estilos CSS para el efecto Neón y Video de fondo
st.markdown(
    f"""
    <style>
    /* Ocultar elementos de la interfaz de Streamlit */
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
        padding-top: 20vh;
        font-family: 'Arial Black', sans-serif;
    }}

    .neon-text {{
        font-size: 5rem;
        font-weight: bold;
        color: #fff;
        text-transform: uppercase;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #ff00ff, 0 0 80px #ff00ff;
    }}
    
    .sub-text {{
        font-size: 2rem;
        font-weight: bold;
        color: #fff;
        text-shadow: 2px 2px 4px #000;
        margin-top: 10px;
    }}

    /* Estilo personalizado para el botón */
    .stButton>button {{
        background-color: rgba(255, 0, 255, 0.7) !important;
        color: white !important;
        border: 2px solid #00ffff !important;
        border-radius: 50px !important;
        padding: 10px 30px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        box-shadow: 0 0 15px #ff00ff;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 30px #00ffff;
        transform: scale(1.05);
    }}
    </style>

    <video autoplay muted loop playsinline class="video-bg">
        <source src="{VIDEO_URL}" type="video/mp4">
        Tu navegador no soporta video.
    </video>

    <div class="main-content">
        <h1 class="neon-text">SALVADOR</h1>
        <p class="sub-text">THE DROP: 15 AÑOS</p>
        <p style="font-size: 1.5rem;">25 DE ABRIL | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Botón de confirmación centrado
st.write("<br>" * 4, unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("CONFIRMAR ASISTENCIA", use_container_width=True):
        st.balloons()
        st.success("¡Confirmación recibida! Salvador te espera.")