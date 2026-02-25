import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Salvador 15: The Drop", layout="wide")

# Estilos CSS
st.markdown(
    """
    <style>
    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    .video-bg {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
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
        font-weight: bold;
        color: #fff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #ff00ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Estructura del Video y Contenido
# Streamlit sirve automáticamente lo que está en 'static'
st.markdown(
    """
    <video autoplay muted loop playsinline class="video-bg">
        <source src="static/invitacion_neon.mp4" type="video/mp4">
    </video>

    <div class="main-content">
        <h1 class="neon-text">SALVADOR</h1>
        <p style="font-size: 2rem;">THE DROP: 25 DE ABRIL</p>
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
        st.success("¡Confirmado! Salvador te espera.")