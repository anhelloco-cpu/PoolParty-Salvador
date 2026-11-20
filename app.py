import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
SUPABASE_URL = "https://pnpwrfjeiqwibkbqmswv.supabase.co"
SUPABASE_KEY = "sb_publishable_7UMYHjae3aVWA1S9_LAkVw_Ot2CJluw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CARGAR CONFIGURACIÓN ACTIVA DESDE EL PANEL ADMIN ---
CONFIG_DEFAULT = {
    "nombre_festejado": "SALVADOR",
    "titulo_pagina": "Pool Party Salvador",
    "subtitulo": "",
    "mostrar_nombre_sobre_foto": False,
    "fecha_cronometro": "April 22, 2026 23:59:59",
    "fecha_texto": "25 de abril",
    "lugar_nombre": "RANCHO JP",
    "direccion": "Barrio el Cañito, Km 1, sobre la Troncal, Monteria.",
    "horario": "Desde el fin del Pre-Icfes hasta el amanecer.",
    "titulo_acordeon": "🔽 VER LUGAR, CANTAUTOR Y DJ",
    "texto_marquesina": "⚡PRESENTACIÓN ESPECIAL:⚡⚡ LEINNER DE LA OSSA Y ROBERTICO LOPEZ ⚡⚡DJ CALAO ⚡⚡",
    "mensaje_exito": "NOS VEMOS EN EL RANCHO.",
    "opciones_comida": "Carne, Pollo, Vegetariano, Sin preferencia",
    "foto_url": "",
    "audio_url": "",
    "color_primario": "#00ffff",
    "color_secundario": "#ff00ff",
    "color_fondo": "#060e1d",
}

cfg = CONFIG_DEFAULT.copy()
try:
    res_cfg = supabase.table("configuracion_invitacion").select("*").eq("id", 1).execute()
    if res_cfg.data:
        for k, v in res_cfg.data[0].items():
            if v is not None:
                cfg[k] = v
except Exception:
    pass

# --- UTILIDADES DE COLOR PARA TRANSPARENCIAS Y CONTRASTE ---
def hex_a_rgba(hex_color, alpha):
    h = (hex_color or "#060e1d").lstrip("#")
    if len(h) != 6:
        return f"rgba(6, 14, 29, {alpha})"
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

def color_texto_contraste(hex_color):
    h = (hex_color or "#ff00ff").lstrip("#")
    if len(h) != 6:
        return "#ffffff"
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    luminancia = (0.299 * r + 0.587 * g + 0.114 * b)
    return "#000000" if luminancia > 175 else "#ffffff"

c_prim = cfg.get("color_primario") or "#00ffff"
c_sec = cfg.get("color_secundario") or "#ff00ff"
c_fond = cfg.get("color_fondo") or "#060e1d"

c_fond_95 = hex_a_rgba(c_fond, 0.95)
c_fond_85 = hex_a_rgba(c_fond, 0.85)
c_prim_12 = hex_a_rgba(c_prim, 0.12)
c_txt_marquesina = color_texto_contraste(c_sec)

# Configuración inicial
st.set_page_config(page_title=cfg["titulo_pagina"], layout="centered", initial_sidebar_state="collapsed")

# 1. FUNCIÓN CARGAR RECURSOS LOCALES (RESPALDO SI NO SE SUBIÓ DESDE EL PANEL)
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

IMAGE_URL = cfg.get("foto_url") or cargar_archivo_local("invitacion.jpg", tipo="image")
AUDIO_DATA = cfg.get("audio_url") or cargar_archivo_local("musica.mp3", tipo="audio")

# --- ESTILOS DINÁMICOS (Adaptados a los colores configurados) ---
st.markdown(f"""
<style>
/* Ocultar menús y ajustar márgenes superiores */
#MainMenu, footer, header {{visibility: hidden;}}
.block-container {{
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
    max-width: 500px !important; 
    margin: 0 auto !important;
}}

div[data-testid="stVerticalBlock"] {{
    gap: 0rem !important; 
}}

/* Botón principal */
div.stButton {{ 
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin-bottom: -5px !important;
}}

div.stButton > button:first-child {{
    background: linear-gradient(135deg, {c_fond}, {c_prim}) !important;
    color: white !important; 
    border: 2px solid {c_prim} !important;
    border-radius: 50px !important; 
    padding: 10px 15px !important;
    font-size: 0.85rem !important; 
    font-weight: 900 !important;
    text-transform: uppercase !important; 
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.75) !important;
    box-shadow: 0 0 15px {c_prim} !important;
    width: auto !important; 
    min-width: 250px !important;
    max-width: 320px !important;
    white-space: nowrap !important; 
}}

/* --- ESTILOS DEL FORMULARIO --- */
.stForm {{ 
    background-color: {c_fond_95} !important; 
    border: 2px solid {c_sec} !important; 
    border-radius: 15px !important; 
    margin-bottom: 0px !important;
    padding: 20px !important;
    box-shadow: 0 0 15px {c_sec} !important;
}}

/* ETIQUETAS EN BLANCO */
div[data-testid="stTextInput"] label p, 
div[data-testid="stSelectbox"] label p {{ 
    color: white !important; 
    font-weight: bold !important; 
    font-size: 0.85rem !important;
    text-transform: uppercase;
}}

/* Cajas de texto y selectbox */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
    background-color: {c_fond} !important;
    color: white !important;
    border: 1px solid {c_sec} !important;
    border-radius: 8px !important;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] span {{
    color: white !important;
}}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {{
    border-color: {c_prim} !important;
    box-shadow: 0 0 8px {c_prim} !important;
}}
</style>
""", unsafe_allow_html=True)

# --- 2. LÓGICA DE REGISTRO ---
if 'confirmando' not in st.session_state: 
    st.session_state.confirmando = False

if not st.session_state.confirmando:
    if st.button("CONFIRMAR ASISTENCIA"):
        st.session_state.confirmando = True
        st.rerun()

if st.session_state.confirmando:
    opciones_lista = [x.strip() for x in cfg["opciones_comida"].split(",") if x.strip()]
    if not opciones_lista:
        opciones_lista = ["Carne", "Pollo", "Vegetariano", "Sin preferencia"]

    with st.form("registro"):
        st.markdown(
            f"<h3 style='text-align:center; color:{c_sec}; text-shadow: 0 0 10px {c_sec}; margin-bottom: 20px;'>ESCRIBE TUS DATOS</h3>",
            unsafe_allow_html=True
        )
        
        nom = st.text_input("Nombre")
        ape = st.text_input("Apellido")
        gusto_form = st.selectbox("Preferencia de Comida", opciones_lista)
        cancion = st.text_input("Tu canción favorita")
        
        st.write("")
        
        c1, c2 = st.columns(2)
        with c1:
            submit_btn = st.form_submit_button("REGISTRARME", use_container_width=True)
        with c2:
            back_btn = st.form_submit_button("VOLVER", use_container_width=True)
            
        if submit_btn:
            if nom and ape:
                try:
                    supabase.table("invitados_pool_party").insert({
                        "nombre": nom, 
                        "apellido": ape,
                        "gusto_comida": gusto_form,
                        "disco_preferido": cancion
                    }).execute()
                    st.snow()
                    st.success(f"¡LISTO {nom.upper()}! {cfg['mensaje_exito']}")
                    st.session_state.confirmando = False
                except Exception:
                    st.error("Error de conexión.")
            else:
                st.warning("El nombre y apellido son obligatorios.")
                
        if back_btn:
            st.session_state.confirmando = False
            st.rerun()

# --- 3. HTML DE LA INVITACIÓN ---
if not IMAGE_URL:
    st.error("❌ No encuentro la imagen de fondo. Súbela desde el panel de configuración.")
else:
    audio_tag = f'<audio id="bgMusic" loop autoplay><source src="{AUDIO_DATA}"></audio>' if AUDIO_DATA else ""

    bloque_nombre = ""
    if cfg.get("mostrar_nombre_sobre_foto"):
        bloque_nombre = f"""
        <div class="host-title">
            <h1>{cfg['nombre_festejado']}</h1>
            <p>{cfg.get('subtitulo', '')}</p>
        </div>
        """

    codigo_html_js = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 0; background-color: {c_fond}; overflow: hidden; font-family: 'Arial Black', sans-serif; }}
        
        .invitation-container {{
            position: relative; 
            width: 100%; 
            height: 100vh; 
            max-width: 500px;
            margin: 0 auto;
        }}

        .invitation-bg {{
            width: 100%;
            height: 100%;
            object-fit: cover; 
            display: block;
            position: absolute;
            top: 0; left: 0;
            z-index: 1;
        }}

        .host-title {{
            position: absolute;
            z-index: 10;
            width: 100%;
            top: 10%;
            left: 0;
            text-align: center;
            color: white;
        }}
        .host-title h1 {{
            margin: 0;
            font-size: 2.5rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            text-shadow: 0 0 12px {c_prim}, 0 0 24px {c_sec};
        }}
        .host-title p {{
            margin: 4px 0 0 0;
            font-size: 0.9rem;
            letter-spacing: 2px;
            color: {c_prim};
            text-shadow: 0 0 8px #000;
        }}

        .overlay-content {{
            position: absolute; 
            z-index: 10; 
            width: 100%; 
            top: 60%; 
            left: 0;
            text-align: center;
        }}
        
        .timer-block {{
            background-color: {c_fond_85}; 
            border: 1px solid {c_prim}; 
            border-radius: 8px; 
            padding: 8px; 
            margin: 0 auto 10px auto;
            width: 65%; 
            box-shadow: 0 0 10px {c_prim};
        }}
        .timer-count {{ font-size: 1.2rem; font-weight: bold; color: {c_prim}; text-shadow: 0 0 8px {c_prim}; }}
        .timer-label {{ font-size: 0.6rem; text-transform: uppercase; color: {c_sec}; }}

        .info-accordion {{
            width: 85%;
            margin: 0 auto;
            background: {c_prim_12};
            border: 1px solid {c_prim}; 
            border-radius: 10px;
            overflow: hidden;
        }}
        summary {{
            padding: 10px; color: {c_prim}; cursor: pointer; outline: none;
            list-style: none; font-size: 0.85rem; font-weight: bold;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.85);
        }}
        .details-content {{ 
            padding: 10px; text-align: left; font-size: 0.75rem; 
            color: white; background: rgba(0,0,0,0.8);
        }}

        .marquee {{
            white-space: nowrap; overflow: hidden; background: {c_sec}; 
            color: {c_txt_marquesina}; margin-top: 10px; padding: 5px 0;
            box-shadow: 0 0 10px {c_sec};
        }}
        .marquee p {{
            display: inline-block; padding-left: 100%;
            animation: marquee 10s linear infinite; margin: 0;
            font-weight: 900; text-transform: uppercase; font-size: 0.8rem;
        }}
        @keyframes marquee {{
            0%   {{ transform: translate(0, 0); }}
            100% {{ transform: translate(-100%, 0); }}
        }}
    </style>
    </head>
    <body>
        {audio_tag}
        
        <div class="invitation-container">
            <img src="{IMAGE_URL}" class="invitation-bg">
            {bloque_nombre}
            
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
                    <summary>{cfg['titulo_acordeon']}</summary>
                    <div class="details-content">
                        <strong style="color:{c_prim};">📍 {cfg['lugar_nombre']}</strong><br>
                        {cfg['direccion']}<br>
                        <strong style="color:{c_prim};">📅 FECHA:</strong> {cfg['fecha_texto']}<br>
                        <strong style="color:{c_sec};">🌅 HORARIO:</strong><br>
                        {cfg['horario']}
                        
                        <div class="marquee">
                            <p>{cfg['texto_marquesina']}</p>
                        </div>
                    </div>
                </details>
            </div>
        </div>

        <script>
            const targetDate = new Date('{cfg['fecha_cronometro']}').getTime();
            const timerInterval = setInterval(() => {{
                const now = new Date().getTime();
                const d = targetDate - now;
                if (d > 0) {{
                    document.getElementById('days').innerText = String(Math.floor(d / 86400000)).padStart(2, '0');
                    document.getElementById('hours').innerText = String(Math.floor((d % 86400000) / 3600000)).padStart(2, '0');
                    document.getElementById('minutes').innerText = String(Math.floor((d % 3600000) / 60000)).padStart(2, '0');
                    document.getElementById('seconds').innerText = String(Math.floor((d % 60000) / 1000)).padStart(2, '0');
                }} else {{
                    clearInterval(timerInterval);
                    document.getElementById('timerBlock').innerHTML = '<div style="color:{c_sec}; font-size:0.9rem; padding:4px;">¡HOY ES LA FIESTA!</div>';
                }}
            }}, 1000);

            document.body.addEventListener('click', () => {{
                const music = document.getElementById('bgMusic');
                if (music) music.play();
            }}, {{ once: true }});
        </script>
    </body>
    </html>
    """
    components.html(codigo_html_js, height=750)