import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
# Ingresa aquí tus credenciales de Settings > API en tu panel de Supabase
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración inicial de la página
st.set_page_config(page_title="Pool Party Salvador", layout="wide", initial_sidebar_state="collapsed")

# 1. FUNCIÓN SABUESO
def cargar_imagen_local(nombre_archivo):
    rutas_posibles = [
        os.path.join(os.path.dirname(__file__), nombre_archivo),
        os.path.join(os.getcwd(), nombre_archivo),
        os.path.join(os.path.dirname(__file__), "static", nombre_archivo)
    ]
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            with open(ruta, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded_string}", None
    return None, rutas_posibles[0]

# Cargar la imagen
IMAGE_URL, ruta_error = cargar_imagen_local("invitacion.jpg")

if not IMAGE_URL:
    st.error("❌ Aún no encuentro la imagen.")
else:
    # 2. EL CÓDIGO HTML Y JS MEJORADO
    codigo_html_js = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 0; background-color: #060e1d; overflow: hidden; }}
        .invitation-container {{
            position: relative; width: 100%; max-width: 500px;
            margin: 0 auto; overflow: hidden; background-color: #060e1d;
            aspect-ratio: 9 / 16;
        }}
        .invitation-bg {{
            width: 100%; height: 100%; object-fit: cover; position: absolute; z-index: 1;
        }}
        #waterCanvas {{
            position: absolute; bottom: 0; left: 0; width: 100%; height: 35%; z-index: 2;
        }}
        .overlay-content {{
            position: absolute; z-index: 10; width: 100%; top: 62%; 
            text-align: center; color: white; font-family: 'Arial Black', sans-serif;
        }}
        .timer-block {{
            background-color: rgba(6, 14, 29, 0.85); border: 2px solid #00ffff;
            border-radius: 10px; padding: 15px; width: 85%; margin: 0 auto;
            box-shadow: 0 0 15px #ff00ff;
        }}
        .timer-label {{ font-size: 0.85rem; text-transform: uppercase; color: #ff00ff; margin-top: 5px; }}
        .timer-count {{ font-size: 2.2rem; font-weight: bold; color: #00ffff; text-shadow: 0 0 10px #00ffff; }}
    </style>
    </head>
    <body>
        <div class="invitation-container">
            <img src="{IMAGE_URL}" class="invitation-bg" id="bgImage" alt="Fondo Salvador">
            <canvas id="waterCanvas"></canvas>
            <div class="overlay-content">
                <div class="timer-block" id="timerBlock">
                    <div style="display: flex; justify-content: space-around;">
                        <div><div class="timer-count" id="days">00</div><div class="timer-label">Días</div></div>
                        <div><div class="timer-count" id="hours">00</div><div class="timer-label">Hrs</div></div>
                        <div><div class="timer-count" id="minutes">00</div><div class="timer-label">Min</div></div>
                        <div><div class="timer-count" id="seconds">00</div><div class="timer-label">Seg</div></div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdnjs.github.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const targetDate = new Date('April 22, 2026 23:59:59').getTime();
            const daysEl = document.getElementById('days');
            const hoursEl = document.getElementById('hours');
            const minutesEl = document.getElementById('minutes');
            const secondsEl = document.getElementById('seconds');
            const timerBlock = document.getElementById('timerBlock');

            function updateTimer() {{
                const now = new Date().getTime();
                const distance = targetDate - now;
                if (distance > 0) {{
                    daysEl.innerText = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
                    hoursEl.innerText = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
                    minutesEl.innerText = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
                    secondsEl.innerText = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');
                }} else {{
                    timerBlock.innerHTML = '<h3 style="font-size: 1.8rem; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; margin:0;">¡LA FIESTA ES HOY!</h3>';
                }}
            }}
            updateTimer();
            setInterval(updateTimer, 1000);

            const canvas = document.getElementById('waterCanvas');
            const ctx = canvas.getContext('2d');
            const img = document.getElementById('bgImage');

            function startWaterAnimation() {{
                canvas.width = canvas.parentElement.offsetWidth;
                canvas.height = canvas.parentElement.offsetHeight * 0.35;
                ctx.save();
                ctx.beginPath();
                ctx.rect(0, 0, canvas.width, canvas.height);
                ctx.clip();
                ctx.drawImage(img, 0, -canvas.parentElement.offsetHeight * 0.65, canvas.width, canvas.parentElement.offsetHeight);
                ctx.restore();
                if (typeof anime !== 'undefined') {{
                    anime({{
                        targets: canvas,
                        translateY: ['-2px', '3px', '-2px'],
                        opacity: [1, 0.8, 1],
                        duration: 3500,
                        easing: 'easeInOutSine',
                        loop: true
                    }});
                }}
            }}
            if(img.complete) {{ startWaterAnimation(); }} else {{ img.onload = startWaterAnimation; }}
        }});
        </script>
    </body>
    </html>
    """
    components.html(codigo_html_js, height=800)

# 3. ESTILOS DEL BOTÓN Y FORMULARIO
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.stButton {
    text-align: center;
    margin-top: -50px;
    position: relative;
    z-index: 100;
}

/* Botón Principal Aqua-Neon */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #001f3f 0%, #0074D9 50%, #00ffff 100%) !important;
    color: white !important;
    border: 2px solid #00ffff !important;
    border-radius: 50px !important;
    padding: 15px 35px !important;
    font-size: 1.3rem !important;
    font-weight: 900 !important;
    font-family: 'Arial Black', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    box-shadow: 0 0 20px #00ffff, inset 0 0 10px rgba(255,255,255,0.4) !important;
    width: 100%;
    max-width: 450px;
    margin: 0 auto;
    display: block;
}

div.stButton > button:hover {
    box-shadow: 0 0 40px #00ffff, 0 0 10px #ff00ff !important;
    transform: scale(1.02);
}

/* Estilos para el Formulario Neón */
.stForm {
    background-color: #060e1d !important;
    border: 2px solid #ff00ff !important;
    box-shadow: 0 0 20px #ff00ff !important;
    border-radius: 15px !important;
    padding: 20px !important;
}

input {
    background-color: #0b1a33 !important;
    color: #00ffff !important;
    border: 1px solid #00ffff !important;
}

label {
    color: #00ffff !important;
    font-family: 'Arial Black', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE REGISTRO (Corregida para evitar globos y forzar datos)
if 'confirmando' not in st.session_state:
    st.session_state.confirmando = False

# Solo mostramos el botón azul si NO se está llenando el formulario
if not st.session_state.confirmando:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # AQUÍ ESTÁ EL CAMBIO: El botón solo activa el formulario, no lanza globos.
        if st.button("CONFIRMAR ASISTENCIA"):
            st.session_state.confirmando = True
            st.rerun()

# Si el usuario activó la confirmación, aparece el formulario
if st.session_state.confirmando:
    with st.form("form_registro", clear_on_submit=True):
        st.markdown("<h3 style='text-align:center; color:#ff00ff; text-shadow: 0 0 10px #ff00ff;'>LISTA DE INVITADOS</h3>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        nombre_form = c1.text_input("Nombre")
        apellido_form = c2.text_input("Apellido")
        
        gusto_form = st.selectbox("Preferencia de Comida", ["Carne", "Pollo", "Vegetariano", "Sin preferencia"])
        disco_form = st.text_input("Tu canción favorita")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            enviar_datos = st.form_submit_button("REGISTRARME AHORA")
        with col_f2:
            cancelar_form = st.form_submit_button("VOLVER")
        
        if enviar_datos:
            if nombre_form and apellido_form:
                datos_save = {
                    "nombre": nombre_form,
                    "apellido": apellido_form,
                    "gusto_comida": gusto_form,
                    "disco_preferido": disco_form
                }
                try:
                    supabase.table("invitados_pool_party").insert(datos_save).execute()
                    # EFECTO LÁSER/LUCES (st.snow simula partículas de luz neón)
                    st.snow() 
                    st.success(f"¡BRUTAL {nombre_form.upper()}! REGISTRO COMPLETADO.")
                    st.session_state.confirmando = False
                except Exception as e:
                    st.error("Error de conexión. Inténtalo de nuevo.")
            else:
                st.warning("Nombre y apellido son requeridos para la lista.")
        
        if cancelar_form:
            st.session_state.confirmando = False
            st.rerun()