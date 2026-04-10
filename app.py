import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración inicial de la página
st.set_page_config(page_title="Pool Party Salvador", layout="wide", initial_sidebar_state="collapsed")

# 1. FUNCIÓN SABUESO (Para imagen y audio)
def cargar_archivo_local(nombre_archivo, tipo="image"):
    rutas_posibles = [
        os.path.join(os.path.dirname(__file__), nombre_archivo),
        os.path.join(os.getcwd(), nombre_archivo),
        os.path.join(os.path.dirname(__file__), "static", nombre_archivo)
    ]
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            with open(ruta, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            if tipo == "image":
                return f"data:image/jpeg;base64,{encoded_string}"
            else:
                return f"data:audio/mpeg;base64,{encoded_string}"
    return None

# Cargar recursos
IMAGE_URL = cargar_archivo_local("invitacion.jpg")
AUDIO_DATA = cargar_archivo_local("musica.mp3", tipo="audio") 

if not IMAGE_URL:
    st.error("❌ Aún no encuentro la imagen 'invitacion.jpg'.")
else:
    # 2. EL CÓDIGO HTML Y JS (BOTÓN INTEGRADO DENTRO)
    codigo_html_js = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 0; background-color: #060e1d; overflow: hidden; font-family: 'Arial Black', sans-serif; }}
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
            position: absolute; z-index: 10; width: 100%; top: 48%; 
            text-align: center; color: white;
        }}
        
        /* Cronómetro */
        .timer-block {{
            background-color: rgba(6, 14, 29, 0.85); border: 2px solid #00ffff;
            border-radius: 10px; padding: 12px; width: 85%; margin: 0 auto 15px;
            box-shadow: 0 0 15px #00ffff;
        }}
        .timer-count {{ font-size: 2rem; font-weight: bold; color: #00ffff; text-shadow: 0 0 10px #00ffff; }}
        .timer-label {{ font-size: 0.7rem; text-transform: uppercase; color: #ff00ff; }}

        /* BOTÓN DE CONFIRMACIÓN DENTRO DE LA IMAGEN */
        .btn-confirmar {{
            background: linear-gradient(135deg, #001f3f 0%, #0074D9 50%, #00ffff 100%);
            color: white; border: 2px solid #00ffff; border-radius: 50px;
            padding: 12px 20px; font-size: 1rem; font-weight: 900;
            text-transform: uppercase; box-shadow: 0 0 20px #00ffff;
            width: 80%; cursor: pointer; margin-bottom: 15px;
            display: inline-block; text-decoration: none;
        }}
        
        /* Desplegable interactivo */
        .info-accordion {{
            width: 85%; margin: 0 auto;
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid #00ffff; border-radius: 10px;
            overflow: hidden;
        }}
        summary {{
            padding: 8px; color: #00ffff; cursor: pointer; outline: none;
            list-style: none; font-size: 0.85rem; font-weight: bold;
        }}
        .details-content {{ 
            padding: 10px; text-align: left; font-size: 0.7rem; 
            background: rgba(0,0,0,0.7); line-height: 1.4;
        }}

        .marquee {{
            white-space: nowrap; overflow: hidden; background: #ff00ff; 
            color: white; margin-top: 8px; padding: 4px 0;
        }}
        .marquee p {{
            display: inline-block; padding-left: 100%;
            animation: marquee 10s linear infinite; margin: 0;
            font-weight: 900;
        }}
        @keyframes marquee {{
            0%   {{ transform: translate(0, 0); }}
            100% {{ transform: translate(-100%, 0); }}
        }}
    </style>
    </head>
    <body>
        <audio id="bgMusic" loop autoplay><source src="{AUDIO_DATA}" type="audio/mpeg"></audio>

        <div class="invitation-container">
            <img src="{IMAGE_URL}" class="invitation-bg" id="bgImage">
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

                <button class="btn-confirmar" onclick="parent.window.confirmarAsistencia()">
                    CONFIRMAR ASISTENCIA
                </button>

                <details class="info-accordion">
                    <summary>🔽 VER LUGAR Y DJ</summary>
                    <div class="details-content">
                        <strong style="color:#00ffff;">📍 RANCHO JP</strong><br>
                        Barrio el Cañito, Km 1, sobre la Troncal, Monteria-Ciénaga de Oro.<br>
                        <strong style="color:#ff00ff;">🌅 HORARIO:</strong><br>
                        Desde que termine el Pre-Icfes hasta el amanecer.
                        <div class="marquee"><p>⚡ DJ CALAO EN VIVO ⚡ DJ CALAO ⚡</p></div>
                    </div>
                </details>
            </div>
        </div>

        <script src="https://cdnjs.github.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
        <script>
            const targetDate = new Date('April 22, 2026 23:59:59').getTime();
            function updateTimer() {{
                const now = new Date().getTime();
                const distance = targetDate - now;
                if (distance > 0) {{
                    document.getElementById('days').innerText = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
                    document.getElementById('hours').innerText = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
                    document.getElementById('minutes').innerText = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
                    document.getElementById('seconds').innerText = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');
                }}
            }}
            updateTimer(); setInterval(updateTimer, 1000);

            const canvas = document.getElementById('waterCanvas');
            const ctx = canvas.getContext('2d');
            const img = document.getElementById('bgImage');
            function startWater() {{
                canvas.width = canvas.parentElement.offsetWidth;
                canvas.height = canvas.parentElement.offsetHeight * 0.35;
                ctx.drawImage(img, 0, -canvas.parentElement.offsetHeight * 0.65, canvas.width, canvas.parentElement.offsetHeight);
                if (typeof anime !== 'undefined') {{
                    anime({{targets: canvas, translateY: ['-2px', '3px'], opacity: [1, 0.8], duration: 3500, easing: 'easeInOutSine', loop: true}});
                }}
            }}
            if(img.complete) {{ startWater(); }} else {{ img.onload = startWater; }}
            document.body.addEventListener('click', () => {{ document.getElementById('bgMusic').play(); }}, {{ once: true }});
        </script>
    </body>
    </html>
    """
    
    # JavaScript para comunicar el botón HTML con Streamlit
    st.components.v1.html(codigo_html_js, height=800)
    
    # Script para recibir el clic del botón HTML
    components.html(
        """
        <script>
        window.confirmarAsistencia = function() {
            window.parent.postMessage({type: 'confirmar'}, '*');
        };
        </script>
        """,
        height=0
    )

# --- LÓGICA DE REGISTRO ---
# Capturar el mensaje del botón HTML
import json
from streamlit_javascript import st_javascript

# Usamos session_state para manejar el flujo
if 'confirmando' not in st.session_state:
    st.session_state.confirmando = False

# Estilos adicionales para ocultar menús y para el formulario
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stForm {
    background-color: #060e1d !important;
    border: 2px solid #ff00ff !important;
    box-shadow: 0 0 20px #ff00ff !important;
    border-radius: 15px !important;
    padding: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# Botón "invisible" que se activa desde el HTML
if st.button("Activar Formulario", key="hidden_btn", help="Solo interno"):
    st.session_state.confirmando = True
    st.rerun()

# --- FORMULARIO ---
if st.session_state.confirmando:
    with st.form("form_registro", clear_on_submit=True):
        st.markdown("<h3 style='text-align:center; color:#ff00ff;'>LISTA DE INVITADOS</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        nombre_form = c1.text_input("Nombre")
        apellido_form = c2.text_input("Apellido")
        gusto_form = st.selectbox("Comida", ["Carne", "Pollo", "Vegetariano", "Sin preferencia"])
        disco_form = st.text_input("¿Qué canción quieres que ponga DJ CALAO?")
        
        col_f1, col_f2 = st.columns(2)
        if col_f1.form_submit_button("REGISTRARME AHORA"):
            if nombre_form and apellido_form:
                try:
                    supabase.table("invitados_pool_party").insert({
                        "nombre": nombre_form, "apellido": apellido_form,
                        "gusto_comida": gusto_form, "disco_preferido": disco_form
                    }).execute()
                    st.snow() 
                    st.success(f"¡LISTO {nombre_form.upper()}! NOS VEMOS EN EL RANCHO JP.")
                    st.session_state.confirmando = False
                except:
                    st.error("Error de conexión.")
            else:
                st.warning("Nombre y apellido son requeridos.")
        
        if col_f2.form_submit_button("VOLVER"):
            st.session_state.confirmando = False
            st.rerun()