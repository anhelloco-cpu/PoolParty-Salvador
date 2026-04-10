import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración inicial
st.set_page_config(page_title="Pool Party Salvador", layout="wide", initial_sidebar_state="collapsed")

# 1. FUNCIÓN CARGAR RECURSOS (Imagen y Audio)
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
            return f"data:{'image/jpeg' if tipo=='image' else 'audio/mpeg'};base64,{encoded_string}"
    return None

IMAGE_URL = cargar_archivo_local("invitacion.jpg")
AUDIO_DATA = cargar_archivo_local("musica.mp3", tipo="audio") 

# --- ESTILOS DEL BOTÓN (Arreglado: sin márgenes negativos que rompan el celular) ---
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

/* Botón centrado, con margen normal abajo para separarlo de la imagen */
.stButton { text-align: center; margin-bottom: 10px; }

div.stButton > button:first-child {
    background: linear-gradient(135deg, #001f3f, #00ffff) !important;
    color: white !important; border: 2px solid #00ffff !important;
    border-radius: 50px !important; padding: 12px 25px !important;
    font-size: 1.1rem !important; font-weight: 900 !important;
    text-transform: uppercase !important; box-shadow: 0 0 20px #00ffff !important;
    width: 80%; max-width: 400px; margin: 0 auto; display: block;
}
.stForm { background-color: #060e1d !important; border: 2px solid #ff00ff !important; border-radius: 15px !important; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE REGISTRO (AHORA ARRIBA DE TODO) ---
if 'confirmando' not in st.session_state: 
    st.session_state.confirmando = False

if not st.session_state.confirmando:
    col1, col2, col3 = st.columns([1, 6, 1])
    if col2.button("CONFIRMAR ASISTENCIA"):
        st.session_state.confirmando = True
        st.rerun()

if st.session_state.confirmando:
    with st.form("registro"):
        st.markdown("<h3 style='text-align:center; color:#ff00ff;'>LISTA DE INVITADOS</h3>", unsafe_allow_html=True)
        nom = st.text_input("Nombre")
        ape = st.text_input("Apellido")
        cancion = st.text_input("¿Qué canción quieres que ponga DJ CALAO?")
        
        c1, c2 = st.columns(2)
        if c1.form_submit_button("REGISTRARME"):
            if nom and ape:
                try:
                    supabase.table("invitados_pool_party").insert({
                        "nombre": nom, 
                        "apellido": ape,
                        "disco_preferido": cancion
                    }).execute()
                    st.snow()
                    st.success(f"¡LISTO {nom.upper()}! NOS VEMOS EN EL RANCHO.")
                    st.session_state.confirmando = False
                except: st.error("Error de conexión.")
            else:
                st.warning("El nombre y apellido son obligatorios.")
                
        if c2.form_submit_button("VOLVER"):
            st.session_state.confirmando = False
            st.rerun()


# --- HTML DE LA INVITACIÓN (ABAJO, SIN INTERFERENCIAS) ---
if not IMAGE_URL:
    st.error("❌ No encuentro 'invitacion.jpg'.")
else:
    # EL CÓDIGO HTML EXACTO QUE TE GUSTÓ (Con el cronómetro más pequeño y el DJ)
    codigo_html_js = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 0; background-color: #060e1d; overflow: hidden; font-family: 'Arial Black', sans-serif; }}
        
        .invitation-container {{
            position: relative; 
            width: 100vw; 
            height: 100vh; 
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #060e1d;
        }}

        .invitation-bg {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain; /* Fiel al diseño original sin distorsión */
            display: block;
        }}

        .overlay-content {{
            position: absolute; 
            z-index: 10; 
            width: 90%; 
            max-width: 450px;
            top: 58%; 
            text-align: center;
        }}
        
        /* CRONÓMETRO MÁS PEQUEÑO Y COMPACTO */
        .timer-block {{
            background-color: rgba(6, 14, 29, 0.9); 
            border: 2px solid #00ffff; 
            border-radius: 8px; 
            padding: 8px; 
            margin: 0 auto 10px auto;
            width: 75%; 
            box-shadow: 0 0 10px #00ffff;
        }}
        .timer-count {{ font-size: 1.3rem; font-weight: bold; color: #00ffff; text-shadow: 0 0 8px #00ffff; }}
        .timer-label {{ font-size: 0.6rem; text-transform: uppercase; color: #ff00ff; }}

        .info-accordion {{
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid #00ffff; 
            border-radius: 10px;
            overflow: hidden;
        }}
        summary {{
            padding: 10px; color: #00ffff; cursor: pointer; outline: none;
            list-style: none; font-size: 0.85rem; font-weight: bold;
        }}
        .details-content {{ 
            padding: 10px; text-align: left; font-size: 0.75rem; 
            color: white; background: rgba(0,0,0,0.8);
        }}

        /* EFECTO DJ CALAO */
        .marquee {{
            white-space: nowrap; overflow: hidden; background: #ff00ff; 
            color: white; margin-top: 10px; padding: 5px 0;
            box-shadow: 0 0 10px #ff00ff;
        }}
        .marquee p {{
            display: inline-block; padding-left: 100%;
            animation: marquee 10s linear infinite; margin: 0;
            font-weight: 900; text-transform: uppercase;
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
            <img src="{IMAGE_URL}" class="invitation-bg">
            
            <div class="overlay-content">
                <div class="timer-block" id="timerBlock">
                    <div style="display: flex; justify-content: space-around;">
                        <div><div class="timer-count" id="days">00</div><div class="timer-label">Días</div></div>
                        <div><div class="timer-count" id="hours">00</div><div class="timer-label">Hrs</div></div>
                        <div><div class="timer-count" id="minutes">00</div><div class="timer-label">Min</div></div>
                        <div><div class="timer-count" id="seconds">00</div><div class="timer-label">Seg</div></div>
                    </div>
                </div>

                <details class="info-accordion">
                    <summary>🔽 VER LUGAR Y DJ</summary>
                    <div class="details-content">
                        <strong style="color:#00ffff;">📍 RANCHO JP</strong><br>
                        Barrio el Cañito, Km 1, sobre la Troncal, Monteria.<br>
                        <strong style="color:#ff00ff;">🌅 HORARIO:</strong><br>
                        Desde el fin del Pre-Icfes hasta el amanecer.
                        
                        <div class="marquee">
                            <p>⚡ PRESENTACIÓN ESPECIAL: DJ CALAO ⚡ DJ CALAO ⚡ DJ CALAO ⚡</p>
                        </div>
                    </div>
                </details>
            </div>
        </div>

        <script>
            const targetDate = new Date('April 22, 2026 23:59:59').getTime();
            setInterval(() => {{
                const now = new Date().getTime();
                const d = targetDate - now;
                if (d > 0) {{
                    document.getElementById('days').innerText = String(Math.floor(d / 86400000)).padStart(2, '0');
                    document.getElementById('hours').innerText = String(Math.floor((d % 86400000) / 3600000)).padStart(2, '0');
                    document.getElementById('minutes').innerText = String(Math.floor((d % 3600000) / 60000)).padStart(2, '0');
                    document.getElementById('seconds').innerText = String(Math.floor((d % 60000) / 1000)).padStart(2, '0');
                }}
            }}, 1000);

            // Iniciar audio al primer clic del usuario
            document.body.addEventListener('click', () => {{
                const music = document.getElementById('bgMusic');
                if (music) music.play();
            }}, {{ once: true }});
        </script>
    </body>
    </html>
    """
    components.html(codigo_html_js, height=750)