import streamlit as st
import base64

# Configuración de la página
st.set_page_config(page_title="The Drop: Salvador 15", layout="wide")

# Función para convertir el video a base64 (necesario para que cargue bien en Streamlit)
def get_video_base64(video_path):
    with open(video_path, "rb") as video_file:
        data = video_file.read()
    return base64.b64encode(data).decode()

# Cambia 'invitacion_neon.mp4' por el nombre exacto de tu archivo si es distinto
try:
    video_base64 = get_video_base64("invitacion_neon.mp4")
    
    # Estilos CSS y Estructura HTML
    st.markdown(
        f"""
        <style>
            /* Quitar márgenes de Streamlit */
            .main {{
                padding: 0;
            }}
            .video-container {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%;
                min-height: 100%;
                z-index: -1;
            }}
            .content {{
                position: relative;
                z-index: 1;
                color: white;
                text-align: center;
                padding-top: 20vh;
                font-family: 'Arial', sans-serif;
            }}
            .neon-title {{
                font-size: 4rem;
                color: #fff;
                text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #ff00ff;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .neon-subtitle {{
                font-size: 1.5rem;
                text-shadow: 0 0 5px #ff00ff;
            }}
            /* Ocultar elementos innecesarios de Streamlit */
            #MainMenu, footer, header {{visibility: hidden;}}
        </style>

        <div class="video-container">
            <video autoplay muted loop playsinline style="width: 100%; height: 100%; object-fit: cover;">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>

        <div class="content">
            <h1 class="neon-title">SALVADOR</h1>
            <p class="neon-subtitle">¡Prepárate para la mejor Pool Party!</p>
            <br>
            <p style="font-size: 1.2rem;">Sábado, 25 de Abril | 2026</p>
        </div>
        """,
        unsafe_allow_html=True
    )

except FileNotFoundError:
    st.error("No encontré el archivo 'invitacion_neon.mp4'. Asegúrate de que esté en la misma carpeta que app.py")

# Aquí puedes añadir más botones de Streamlit si lo deseas
if st.button("Confirmar Asistencia"):
    st.balloons()
    st.success("¡Genial! Salvador te espera.")