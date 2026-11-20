import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO
from datetime import datetime, date, time as dt_time
from fpdf import FPDF
from docx import Document
from PIL import Image
import colorsys
import urllib.request
import base64
import time

# --- CONFIGURACIÓN SUPABASE ---
# Verifica que aquí estén la URL y la KEY de tu proyecto NUEVO de Supabase
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de la página
st.set_page_config(page_title="Panel VIP - Pool Party", layout="wide")

# --- UTILIDADES PARA FECHA JS (INDEPENDIENTE DEL IDIOMA DEL SISTEMA) ---
MESES_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def formatear_fecha_js(fecha_obj, hora_obj):
    mes_en = MESES_EN[fecha_obj.month - 1]
    return f"{mes_en} {fecha_obj.day}, {fecha_obj.year} {hora_obj.strftime('%H:%M:%S')}"

def parsear_fecha_js(fecha_str):
    try:
        partes = fecha_str.replace(",", "").split()
        mes = MESES_EN.index(partes[0]) + 1
        dia = int(partes[1])
        anio = int(partes[2])
        h, m, s = [int(x) for x in partes[3].split(":")]
        return date(anio, mes, dia), dt_time(h, m, s)
    except Exception:
        return date(2026, 4, 22), dt_time(23, 59, 59)

# --- CARGAR CONFIGURACIÓN DE INVITACIÓN DESDE SUPABASE ---
CONFIG_DEFAULT = {
    "id": 1,
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
    "color_fondo": "#060e1d"
}

def cargar_config_invitacion():
    cfg = CONFIG_DEFAULT.copy()
    try:
        res_cfg = supabase.table("configuracion_invitacion").select("*").eq("id", 1).execute()
        if res_cfg.data:
            for k, v in res_cfg.data[0].items():
                if v is not None:
                    cfg[k] = v
    except Exception:
        pass
    return cfg

def subir_archivo_supabase(uploaded_file, prefijo):
    """Sube foto o audio al bucket media_fiestas. Si falla, usa respaldo Base64."""
    archivo_bytes = uploaded_file.getvalue()
    ext = uploaded_file.name.split(".")[-1].lower()
    mime = uploaded_file.type or ("image/jpeg" if prefijo == "fondo" else "audio/mpeg")
    nombre_archivo = f"{prefijo}_{int(time.time())}.{ext}"

    try:
        supabase.storage.from_("media_fiestas").upload(
            path=nombre_archivo,
            file=archivo_bytes,
            file_options={"content-type": mime}
        )
        return supabase.storage.from_("media_fiestas").get_public_url(nombre_archivo)
    except Exception:
        b64 = base64.b64encode(archivo_bytes).decode()
        return f"data:{mime};base64,{b64}"

def obtener_vista_previa(valor_url):
    """Devuelve URL o bytes decodificados para st.image / st.audio."""
    if not valor_url:
        return None
    if valor_url.startswith("data:") and "," in valor_url:
        return base64.b64decode(valor_url.split(",", 1)[1])
    return valor_url

def obtener_bytes_imagen(url_o_b64):
    """Obtiene los bytes de la imagen actual (sea Base64 o URL de Supabase Storage)."""
    if not url_o_b64:
        return None
    if url_o_b64.startswith("data:") and "," in url_o_b64:
        return base64.b64decode(url_o_b64.split(",", 1)[1])
    try:
        req = urllib.request.Request(url_o_b64, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read()
    except Exception:
        return None

def extraer_colores_de_imagen(img_bytes):
    """Extrae (color_primario, color_secundario, color_fondo) armonizados con la foto."""
    try:
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        img.thumbnail((120, 120))
        quant = img.quantize(colors=12)
        palette = quant.getpalette()
        counts = quant.getcolors() or []

        candidatos = []
        for count, idx in counts:
            r, g, b = palette[idx * 3 : idx * 3 + 3]
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            candidatos.append((count, h, s, v))

        if not candidatos:
            return "#00ffff", "#ff00ff", "#060e1d"

        def hsv_a_hex(h, s, v):
            r, g, b = colorsys.hsv_to_rgb(h % 1.0, min(max(s, 0.0), 1.0), min(max(v, 0.0), 1.0))
            return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

        vibrantes = sorted(
            candidatos,
            key=lambda x: (x[2] * (0.4 + 0.6 * x[3])) * (x[0] ** 0.25),
            reverse=True
        )
        _, h1, s1, v1 = vibrantes[0]
        c_primario = hsv_a_hex(h1, max(s1, 0.55) if s1 > 0.12 else s1, max(v1, 0.80))

        sec_elegido = None
        for item in vibrantes[1:]:
            dist_hue = min(abs(item[1] - h1), 1.0 - abs(item[1] - h1))
            if dist_hue >= 0.10 and item[2] >= 0.20:
                sec_elegido = item
                break

        if sec_elegido:
            _, h2, s2, v2 = sec_elegido
            c_secundario = hsv_a_hex(h2, max(s2, 0.55), max(v2, 0.82))
        else:
            c_secundario = hsv_a_hex((h1 + 0.08) % 1.0, max(s1 * 0.8, 0.40), 0.95)

        dominante = max(candidatos, key=lambda x: x[0])
        _, hd, sd, _ = dominante
        c_fondo = hsv_a_hex(hd, min(sd, 0.55), 0.14)

        return c_primario, c_secundario, c_fondo
    except Exception:
        return "#00ffff", "#ff00ff", "#060e1d"

cfg_inv = cargar_config_invitacion()

st.title(f"📋 Panel de Control Financiero - {cfg_inv['titulo_pagina']}")
st.markdown("Gestión de invitados, presupuesto profesional (Costos Fijos vs Variables) y configuración visual de la invitación.")

# --- FUNCIÓN PARA ELIMINAR DUPLICADOS ---
def eliminar_duplicados(df):
    df['nombre_completo'] = (df['nombre'].str.strip() + " " + df['apellido'].str.strip()).str.lower()
    duplicados_a_borrar = df[df.duplicated(subset=['nombre_completo'], keep='first')]
    ids_a_eliminar = duplicados_a_borrar['id'].tolist()
    
    exitos, errores = 0, 0
    for record_id in ids_a_eliminar:
        try:
            supabase.table("invitados_pool_party").delete().eq("id", record_id).execute()
            exitos += 1
        except:
            errores += 1
            
    return exitos, errores

# --- INICIALIZAR MEMORIA DE APORTANTES ---
if 'aportantes' not in st.session_state:
    st.session_state.aportantes = []

# --- CARGA DE DATOS ---
datos = []
error_carga = None
try:
    respuesta = supabase.table("invitados_pool_party").select("*").execute()
    datos = respuesta.data or []
except Exception as e:
    error_carga = e

df = pd.DataFrame(datos) if datos else pd.DataFrame(columns=['nombre', 'apellido', 'gusto_comida', 'disco_preferido'])

# Crear CUATRO pestañas siempre visibles
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 Gestión de Invitados",
    "📊 Presupuesto Profesional",
    "🤝 Financiamiento",
    "⚙️ Configurar Invitación"
])

# ==========================================
# PESTAÑA 1: GESTIÓN DE INVITADOS
# ==========================================
with tab1:
    if error_carga:
        st.error(f"Error de conexión o de datos: {error_carga}")
    elif not datos:
        st.info("Aún no hay invitados registrados en la base de datos.")
        if st.button("🔄 Reintentar"):
            st.rerun()
    else:
        df['nombre_completo'] = (df['nombre'].str.strip() + " " + df['apellido'].str.strip()).str.lower()
        conteo_sobrantes = df.duplicated(subset=['nombre_completo'], keep='first').sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total de Registros (Actual)", value=len(df))
        with col2:
            st.metric(label="Registros Repetidos (Sobrantes)", value=conteo_sobrantes, delta_color="inverse")

        st.divider()

        if conteo_sobrantes > 0:
            st.warning(f"⚠️ Se han detectado {conteo_sobrantes} registros repetidos. Revisa la tabla a continuación:")
            df_mostrar_repetidos = df[df.duplicated(subset=['nombre_completo'], keep=False)].sort_values(by='nombre_completo')
            columnas_revisar = ['nombre', 'apellido', 'gusto_comida', 'disco_preferido']
            if 'created_at' in df.columns:
                columnas_revisar.append('created_at')
            
            st.dataframe(df_mostrar_repetidos[[c for c in columnas_revisar if c in df_mostrar_repetidos.columns]], use_container_width=True)
            
            if st.button("🗑️ CONFIRMAR Y ELIMINAR REPETIDOS"):
                with st.spinner("Limpiando base de datos..."):
                    exitos, errores = eliminar_duplicados(df)
                    if exitos > 0:
                        st.success(f"¡Limpieza completada! Se eliminaron {exitos} registros.")
                        st.rerun()
                    if errores > 0:
                        st.error(f"Hubo problemas eliminando {errores} registros.")
        else:
            st.success("✅ La base de datos está limpia. No hay invitados repetidos.")

        st.divider()
        st.subheader("Lista General de Invitados")
        columnas_visibles = ['nombre', 'apellido', 'gusto_comida', 'disco_preferido']
        st.dataframe(df[[c for c in columnas_visibles if c in df.columns]].sort_values(by='nombre'), use_container_width=True)
        if st.button("🔄 Refrescar Lista"):
            st.rerun()

# ==========================================
# PESTAÑA 2: CALCULADORA PROFESIONAL
# ==========================================
with tab2:
    if not datos:
        st.info("Aún no hay invitados registrados para calcular el presupuesto.")
    else:
        st.header("Estructura de Costos")
        
        if 'config_guardada' not in st.session_state:
            st.session_state.config_guardada = {}
            try:
                res_hist = supabase.table("presupuestos_historicos").select("datos_json").order("fecha_registro", desc=True).limit(1).execute()
                if res_hist.data and res_hist.data[0].get('datos_json'):
                    st.session_state.config_guardada = res_hist.data[0]['datos_json']
            except:
                pass
        
        conf = st.session_state.config_guardada

        conteo_comida = df['gusto_comida'].value_counts()
        total_carne = conteo_comida.get('Carne', 0) + conteo_comida.get('Sin preferencia', 0)
        total_pollo = conteo_comida.get('Pollo', 0)
        total_vege = conteo_comida.get('Vegetariano', 0)
        total_invitados = len(df)
        
        st.info(f"**Invitados Confirmados:** {total_carne} Carne | {total_pollo} Pollo | {total_vege} Veggie | **Total: {total_invitados} personas**")

        with st.form("form_presupuesto"):
            
            st.subheader("📈 COSTOS VARIABLES (Dependen del # de invitados)")
            col_c1, col_c2 = st.columns(2)
            precio_carne = col_c1.number_input("Precio por Kilo Carne ($)", value=int(conf.get('precio_carne', 35000)))
            gr_carne = col_c2.number_input("Gramos carne por persona", value=int(conf.get('gr_carne', 350)))
            
            col_p1, col_p2 = st.columns(2)
            precio_pollo = col_p1.number_input("Precio por Kilo Pollo ($)", value=int(conf.get('precio_pollo', 18000)))
            gr_pollo = col_p2.number_input("Gramos pollo por persona", value=int(conf.get('gr_pollo', 350)))
            
            st.markdown("---")
            st.write("**Pasabocas, Entradas y Acompañamientos**")
            nombre_pasa = st.text_input("Tipo de Pasabocas", value=conf.get('nombre_pasa', "Deditos y empanaditas"))
            col_b1, col_b2, col_b3 = st.columns(3)
            precio_unid_pasa = col_b1.number_input("Precio Unidad Pasaboca ($)", value=int(conf.get('precio_unid_pasa', 1200)))
            unid_persona_ronda = col_b2.number_input("Und. por persona (por ronda)", value=int(conf.get('unid_persona_ronda', 4)))
            num_rondas = col_b3.number_input("Número de rondas", value=int(conf.get('num_rondas', 2)))
            
            col_a1, col_a2 = st.columns(2)
            costo_entrada_pp = col_a1.number_input("Costo Entrada p/p ($)", value=int(conf.get('costo_entrada_pp', 8000)))
            costo_acompa = col_a2.number_input("Acompañamientos p/p ($) (Yuca, papa, etc.)", value=int(conf.get('costo_acompa', 6000)))
            
            presu_bebidas = st.number_input("Presupuesto Bebidas e Hielo ($)", value=int(conf.get('presu_bebidas', 250000)))
            
            st.divider()

            st.subheader("📌 COSTOS FIJOS (Independientes de la asistencia)")
            col_f1, col_f2 = st.columns(2)
            costo_lugar = col_f1.number_input(f"Alquiler del Lugar / {cfg_inv['lugar_nombre']} ($)", value=int(conf.get('costo_lugar', 500000)), step=50000)
            costo_torta = col_f2.number_input("Costo de la Torta ($)", value=int(conf.get('costo_torta', 150000)), step=10000)
            
            col_f3, col_f4 = st.columns(2)
            costo_dj = col_f3.number_input("DJ y Sonido ($)", value=int(conf.get('costo_dj', 250000)), step=10000)
            costo_deco = col_f4.number_input("Decoración Neón y Ambientación ($)", value=int(conf.get('costo_deco', 100000)), step=10000)
            
            st.divider()
            margen = st.slider("Margen Financiero para Imprevistos (%)", 0, 20, int(conf.get('margen', 10)))
            
            generar = st.form_submit_button("💰 GENERAR INFORME FINANCIERO")

        if generar:
            k_carne = (total_carne * gr_carne) / 1000
            gasto_carne = k_carne * precio_carne
            k_pollo = (total_pollo * gr_pollo) / 1000
            gasto_pollo = k_pollo * precio_pollo
            
            total_unidades_pasa = total_invitados * unid_persona_ronda * num_rondas
            gasto_pasabocas = total_unidades_pasa * precio_unid_pasa
            gasto_entradas = total_invitados * costo_entrada_pp
            gasto_acompa = total_invitados * costo_acompa
            
            total_variables = gasto_carne + gasto_pollo + gasto_pasabocas + gasto_entradas + gasto_acompa + presu_bebidas
            total_fijos = costo_lugar + costo_torta + costo_dj + costo_deco
            subtotal = total_variables + total_fijos
            monto_imprevistos = subtotal * (margen / 100)
            gran_total = subtotal + monto_imprevistos
            cuota_por_persona = gran_total / total_invitados if total_invitados > 0 else 0
            
            st.session_state.resultados = {
                "k_carne": k_carne, "gasto_carne": gasto_carne, "k_pollo": k_pollo, "gasto_pollo": gasto_pollo,
                "total_unidades_pasa": total_unidades_pasa, "gasto_pasabocas": gasto_pasabocas,
                "gasto_entradas": gasto_entradas, "gasto_acompa": gasto_acompa, 
                "total_variables": total_variables, "total_fijos": total_fijos,
                "subtotal": subtotal, "monto_imprevistos": monto_imprevistos, "gran_total": gran_total,
                "cuota_por_persona": cuota_por_persona
            }
            
            st.session_state.config_guardada = {
                "precio_carne": precio_carne, "gr_carne": gr_carne, "precio_pollo": precio_pollo, 
                "gr_pollo": gr_pollo, "nombre_pasa": nombre_pasa, "precio_unid_pasa": precio_unid_pasa, 
                "unid_persona_ronda": unid_persona_ronda, "num_rondas": num_rondas, 
                "costo_entrada_pp": costo_entrada_pp, "costo_torta": costo_torta,
                "costo_acompa": costo_acompa, "presu_bebidas": presu_bebidas, 
                "costo_lugar": costo_lugar, "costo_dj": costo_dj, "costo_deco": costo_deco, "margen": margen
            }

        if 'resultados' in st.session_state:
            res = st.session_state.resultados
            conf = st.session_state.config_guardada
            
            st.divider()
            st.subheader("📊 Resumen Ejecutivo")
            
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Kilos Carne", f"{res['k_carne']:.1f} kg")
            r2.metric("Kilos Pollo", f"{res['k_pollo']:.1f} kg")
            r3.metric("Total Pasabocas", f"{res['total_unidades_pasa']} und")
            r4.metric("Cuota Est. p/p", f"${res['cuota_por_persona']:,.0f}")

            resumen_print = f"""
            ### 📝 REPORTE FINANCIERO: {cfg_inv['titulo_pagina'].upper()}
            ---
            **Asistencia Proyectada:** {total_invitados} personas
            
            **1. COSTOS VARIABLES:**
- Proteína (Carne {res['k_carne']:.1f}kg + Pollo {res['k_pollo']:.1f}kg): **${(res['gasto_carne'] + res['gasto_pollo']):,.0f}**
- Entradas: **${res.get('gasto_entradas', 0):,.0f}**
- Pasabocas ({conf['nombre_pasa']} - {res['total_unidades_pasa']} unds): **${res['gasto_pasabocas']:,.0f}**
- Acompañamientos: **${res['gasto_acompa']:,.0f}**
- Bebidas e Hielo: **${conf['presu_bebidas']:,.0f}**
- **Subtotal Variables: ${res['total_variables']:,.0f}**
            
            **2. COSTOS FIJOS:**
- Alquiler de Locación ({cfg_inv['lugar_nombre']}): **${conf['costo_lugar']:,.0f}**
- Torta: **${conf.get('costo_torta', 0):,.0f}**
- DJ y Sistema de Sonido: **${conf['costo_dj']:,.0f}**
- Decoración Neón y Ambientación: **${conf['costo_deco']:,.0f}**
- **Subtotal Fijos: ${res['total_fijos']:,.0f}**
            
            **3. CONSOLIDADO:**
- Subtotal Operativo: ${res['subtotal']:,.0f}
- Fondo de Imprevistos ({conf['margen']}%): ${res['monto_imprevistos']:,.0f}
            
            ### **VALOR TOTAL DEL PROYECTO: ${res['gran_total']:,.0f}**
            """
            
            if st.session_state.aportantes:
                resumen_print += "\n---\n**4. FINANCIAMIENTO Y APORTES:**\n"
                total_recogido = 0
                for ap in st.session_state.aportantes:
                    resumen_print += f"* {ap['nombre']} ({ap['detalle']}): **${ap['monto']:,.0f}**\n"
                    total_recogido += ap['monto']
                resumen_print += f"\n* **Total Recaudado: ${total_recogido:,.0f}**\n"
                resumen_print += f"* **Faltante por cubrir: ${(res['gran_total'] - total_recogido):,.0f}**\n"
            
            resumen_print += f"\n---\n*Punto de equilibrio (Cuota sugerida por invitado): ${res['cuota_por_persona']:,.0f}*"
            
            st.markdown(resumen_print)
            
            st.button("🖨️ PREPARAR PARA IMPRIMIR (Ctrl + P)", on_click=lambda: st.info("Usa Ctrl + P (o Cmd + P en Mac) para guardar este reporte en PDF o imprimirlo."))

            st.divider()
            st.subheader("💾 Opciones de Exportación")
            col_d1, col_d2, col_d3 = st.columns(3)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            for linea in resumen_print.split('\n'):
                texto_limpio = linea.replace('**', '').replace('### ', '').replace('---', '-'*50)
                texto_limpio = texto_limpio.encode('latin-1', 'ignore').decode('latin-1').strip()
                if texto_limpio:
                    pdf.cell(0, 7, txt=texto_limpio, ln=True)
            
            try:
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            except AttributeError:
                pdf_bytes = bytes(pdf.output())

            col_d1.download_button(label="📄 Descargar como PDF", data=pdf_bytes, file_name="Presupuesto_PoolParty.pdf", mime="application/pdf")

            doc = Document()
            doc.add_heading(f"Reporte Financiero - {cfg_inv['titulo_pagina']}", 0)
            for linea in resumen_print.split('\n'):
                texto_limpio = linea.replace('**', '').replace('### ', '').replace('---', '-'*50).replace('📝', '').strip()
                if texto_limpio:
                    doc.add_paragraph(texto_limpio)
            b = BytesIO()
            doc.save(b)
            word_bytes = b.getvalue()

            col_d2.download_button(label="📝 Descargar como Word", data=word_bytes, file_name="Presupuesto_PoolParty.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            datos_guardar = {
                "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_invitados": total_invitados,
                "costos_variables": float(res['total_variables']),
                "costos_fijos": float(res['total_fijos']),
                "gran_total": float(res['gran_total']),
                "cuota_por_persona": float(res['cuota_por_persona']),
                "datos_json": conf 
            }

            if col_d3.button("☁️ Guardar Presupuesto en Supabase"):
                try:
                    supabase.table("presupuestos_historicos").insert(datos_guardar).execute()
                    st.success("✅ ¡Guardado! La próxima vez que entres, los precios se cargarán solos.")
                    st.balloons()
                except Exception as e:
                    st.error(f"⚠️ Necesitas agregar una columna llamada 'datos_json' (tipo JSONB) en la tabla 'presupuestos_historicos'. Error: {e}")

# ==========================================
# PESTAÑA 3: FINANCIAMIENTO 
# ==========================================
with tab3:
    st.header("🤝 Gestión de Aportes y Financiamiento")
    
    if 'resultados' not in st.session_state:
        st.warning("⚠️ Primero debes ir a la pestaña 'Presupuesto Profesional' y darle al botón de Generar Informe para conocer el costo total de la fiesta.")
    else:
        res = st.session_state.resultados
        conf = st.session_state.config_guardada
        gran_total = res['gran_total']
        
        st.metric("Meta de Recaudo (Costo Total de la Fiesta)", f"${gran_total:,.0f}")
        st.divider()

        with st.form("form_aportes"):
            st.subheader("Asignar un Patrocinador o Responsable")
            
            c_resp1, c_resp2 = st.columns(2)
            nombre_aportante = c_resp1.text_input("Nombre de la Persona (Ej. Mamá, Yo, Tío Juan)")
            
            tipo_aporte = c_resp2.selectbox("Tipo de Aporte", [
                "Asumir un Gasto Específico", 
                "Monto Fijo ($)", 
                "Porcentaje del Total General (%)",
                "Porcentaje del Saldo Faltante (%)"
            ])
            
            st.markdown("---")
            st.write("**Detalles del Aporte**")
            
            c_det1, c_det2, c_det3 = st.columns(3)
            
            gastos_disponibles = {
                "Proteína (Carne y Pollo)": res['gasto_carne'] + res['gasto_pollo'],
                "Entradas": res.get('gasto_entradas', 0),
                f"Pasabocas ({conf['nombre_pasa']})": res['gasto_pasabocas'],
                "Acompañamientos": res['gasto_acompa'],
                "Bebidas e Hielo": conf['presu_bebidas'],
                "Alquiler de Locación": conf['costo_lugar'],
                "Torta": conf.get('costo_torta', 0),
                "DJ y Sonido": conf['costo_dj'],
                "Decoración": conf['costo_deco'],
                "Fondo de Imprevistos": res['monto_imprevistos']
            }
            
            item_especifico = c_det1.selectbox("Si eligió 'Gasto Específico', ¿Qué va a pagar?", ["Seleccionar..."] + list(gastos_disponibles.keys()))
            monto_fijo = c_det2.number_input("Si eligió 'Monto Fijo', escribe el valor ($)", value=0, step=50000)
            porcentaje_fijo = c_det3.number_input("Si eligió 'Porcentaje', escribe el %", value=0, max_value=100)
            
            agregar_aporte = st.form_submit_button("➕ AGREGAR AL RECAUDO")
            
        if agregar_aporte:
            if not nombre_aportante:
                st.error("Por favor escribe el nombre de la persona.")
            else:
                valor_calculado = 0
                detalle_texto = ""
                
                if tipo_aporte == "Asumir un Gasto Específico" and item_especifico != "Seleccionar...":
                    valor_calculado = gastos_disponibles[item_especifico]
                    detalle_texto = f"Pago de {item_especifico}"
                    
                elif tipo_aporte == "Monto Fijo ($)" and monto_fijo > 0:
                    valor_calculado = monto_fijo
                    detalle_texto = "Aporte de monto fijo"
                    
                elif tipo_aporte == "Porcentaje del Total General (%)" and porcentaje_fijo > 0:
                    valor_calculado = gran_total * (porcentaje_fijo / 100)
                    detalle_texto = f"Aporte del {porcentaje_fijo}% del total general"
                    
                elif tipo_aporte == "Porcentaje del Saldo Faltante (%)" and porcentaje_fijo > 0:
                    recogido_hasta_ahora = sum(ap['monto'] for ap in st.session_state.aportantes)
                    saldo_actual = gran_total - recogido_hasta_ahora
                    
                    if saldo_actual <= 0:
                        st.error("¡El presupuesto ya está cubierto en su totalidad! No hay saldo faltante.")
                        valor_calculado = 0
                    else:
                        valor_calculado = saldo_actual * (porcentaje_fijo / 100)
                        detalle_texto = f"Aporte del {porcentaje_fijo}% del saldo faltante"
                        
                else:
                    st.error("Verifica los datos del aporte. Selecciona un item, un monto o un porcentaje mayor a 0.")
                    valor_calculado = 0
                    
                if valor_calculado > 0:
                    st.session_state.aportantes.append({
                        "nombre": nombre_aportante,
                        "detalle": detalle_texto,
                        "monto": valor_calculado
                    })
                    st.success(f"¡Aporte de {nombre_aportante} agregado exitosamente!")
                    st.rerun()

        if st.session_state.aportantes:
            st.subheader("📈 Balance Financiero")
            df_aportes = pd.DataFrame(st.session_state.aportantes)
            total_recogido = df_aportes['monto'].sum()
            faltante = gran_total - total_recogido
            
            c_bal1, c_bal2 = st.columns(2)
            c_bal1.metric("Dinero Asegurado", f"${total_recogido:,.0f}")
            
            if faltante > 0:
                c_bal2.metric("Faltante por Cubrir", f"${faltante:,.0f}", delta="Aún falta", delta_color="inverse")
            elif faltante < 0:
                c_bal2.metric("Sobrante a favor", f"${abs(faltante):,.0f}", delta="¡Superaron la meta!", delta_color="normal")
            else:
                c_bal2.metric("Faltante por Cubrir", "$0", delta="¡Presupuesto Exacto Cubierto!", delta_color="normal")
            
            progreso = min(total_recogido / gran_total, 1.0)
            st.progress(progreso)
            
            st.write("**Lista de Responsables:**")
            
            df_aportes_mostrar = df_aportes.copy()
            df_aportes_mostrar['monto'] = df_aportes_mostrar['monto'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(df_aportes_mostrar, use_container_width=True)
            
            if st.button("🗑️ Limpiar Lista de Aportes"):
                st.session_state.aportantes = []
                st.rerun()

# ==========================================
# PESTAÑA 4: CONFIGURAR INVITACIÓN (COLORES MANUALES O AUTOMÁTICOS)
# ==========================================
with tab4:
    st.header("⚙️ Configuración Visual de la Invitación")
    st.caption("Configura el festejado, fecha, lugar, foto, música y colores de las líneas.")

    fecha_actual, hora_actual = parsear_fecha_js(cfg_inv.get("fecha_cronometro", "April 22, 2026 23:59:59"))

    with st.form("form_config_invitacion"):
        st.subheader("1. Identidad del Evento")
        ci1, ci2 = st.columns(2)
        nombre_festejado = ci1.text_input("Nombre del Festejado / Anfitrión", value=cfg_inv["nombre_festejado"])
        titulo_pagina = ci2.text_input("Título de la Pestaña Web", value=cfg_inv["titulo_pagina"])

        ci3, ci4 = st.columns([2, 1])
        subtitulo = ci3.text_input("Subtítulo sobre la foto (opcional)", value=cfg_inv["subtitulo"])
        mostrar_nombre = ci4.checkbox(
            "Mostrar nombre encima de la foto",
            value=bool(cfg_inv["mostrar_nombre_sobre_foto"])
        )

        st.divider()
        st.subheader("2. Fecha, Lugar y Detalles")
        cf1, cf2, cf3 = st.columns(3)
        fecha_evento = cf1.date_input("Fecha para el Cronómetro", value=fecha_actual)
        hora_evento = cf2.time_input("Hora límite del Cronómetro", value=hora_actual)
        fecha_texto = cf3.text_input("Fecha visible en el acordeón", value=cfg_inv["fecha_texto"])

        cl1, cl2 = st.columns(2)
        lugar_nombre = cl1.text_input("Nombre del Sitio", value=cfg_inv["lugar_nombre"])
        direccion = cl2.text_input("Dirección", value=cfg_inv["direccion"])

        ch1, ch2 = st.columns(2)
        horario = ch1.text_input("Horario", value=cfg_inv["horario"])
        titulo_acordeon = ch2.text_input("Texto del botón desplegable", value=cfg_inv["titulo_acordeon"])

        texto_marquesina = st.text_input("Texto en movimiento (DJ / Artistas / Especiales)", value=cfg_inv["texto_marquesina"])

        cm1, cm2 = st.columns(2)
        mensaje_exito = cm1.text_input("Mensaje al confirmar asistencia", value=cfg_inv["mensaje_exito"])
        opciones_comida = cm2.text_input("Opciones de comida (separadas por coma)", value=cfg_inv["opciones_comida"])

        st.divider()
        st.subheader("3. Multimedia (Foto de Fondo y Disco)")
        cu1, cu2 = st.columns(2)
        nueva_foto = cu1.file_uploader("Subir nueva Foto de Fondo (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
        nuevo_audio = cu2.file_uploader("Subir nuevo Disco / Música (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

        st.divider()
        st.subheader("4. Colores de Líneas, Botón y Marcos")
        modo_color = st.radio(
            "¿Cómo quieres elegir los colores?",
            ["🎨 Manual (uso los colores elegidos abajo)", "✨ Automático (tomar colores de la foto de fondo)"],
            horizontal=True
        )
        cc1, cc2, cc3 = st.columns(3)
        color_primario = cc1.color_picker("Color Principal (Líneas, Botón, Números)", value=cfg_inv.get("color_primario", "#00ffff"))
        color_secundario = cc2.color_picker("Color Secundario (Detalles, Formulario, Banda)", value=cfg_inv.get("color_secundario", "#ff00ff"))
        color_fondo = cc3.color_picker("Color Base Oscuro (Fondo de Tarjetas)", value=cfg_inv.get("color_fondo", "#060e1d"))

        guardar_cfg = st.form_submit_button("💾 GUARDAR Y PUBLICAR INVITACIÓN", use_container_width=True)

    if guardar_cfg:
        with st.spinner("Guardando configuración y procesando colores..."):
            foto_url_final = cfg_inv.get("foto_url", "")
            audio_url_final = cfg_inv.get("audio_url", "")

            if nueva_foto is not None:
                foto_url_final = subir_archivo_supabase(nueva_foto, "fondo")

            if nuevo_audio is not None:
                audio_url_final = subir_archivo_supabase(nuevo_audio, "musica")

            c_prim, c_sec, c_fond = color_primario, color_secundario, color_fondo
            if modo_color.startswith("✨"):
                img_bytes = nueva_foto.getvalue() if nueva_foto is not None else obtener_bytes_imagen(foto_url_final)
                if img_bytes:
                    c_prim, c_sec, c_fond = extraer_colores_de_imagen(img_bytes)
                else:
                    st.warning("No se encontró una foto cargada para extraer colores; se guardaron los colores manuales.")

            payload = {
                "id": 1,
                "nombre_festejado": nombre_festejado.strip() or "INVITADO",
                "titulo_pagina": titulo_pagina.strip() or f"Fiesta de {nombre_festejado}",
                "subtitulo": subtitulo.strip(),
                "mostrar_nombre_sobre_foto": mostrar_nombre,
                "fecha_cronometro": formatear_fecha_js(fecha_evento, hora_evento),
                "fecha_texto": fecha_texto.strip(),
                "lugar_nombre": lugar_nombre.strip(),
                "direccion": direccion.strip(),
                "horario": horario.strip(),
                "titulo_acordeon": titulo_acordeon.strip(),
                "texto_marquesina": texto_marquesina.strip(),
                "mensaje_exito": mensaje_exito.strip(),
                "opciones_comida": opciones_comida.strip() or "Carne, Pollo, Vegetariano, Sin preferencia",
                "foto_url": foto_url_final,
                "audio_url": audio_url_final,
                "color_primario": c_prim,
                "color_secundario": c_sec,
                "color_fondo": c_fond,
                "updated_at": datetime.now().isoformat()
            }

            try:
                supabase.table("configuracion_invitacion").upsert(payload).execute()
                st.success(f"✅ ¡Guardado para **{payload['nombre_festejado']}**! Paleta activa: `{c_prim}` | `{c_sec}` | `{c_fond}`")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar en Supabase. Detalle: {e}")

    st.divider()
    st.subheader("👁️ Vista Previa Actual")
    vp1, vp2 = st.columns(2)
    with vp1:
        st.markdown("**Foto de fondo activa:**")
        prev_foto = obtener_vista_previa(cfg_inv.get("foto_url"))
        if prev_foto:
            st.image(prev_foto, width=260)
        else:
            st.info("Usando la imagen local por defecto (`invitacion.jpg`).")
    with vp2:
        st.markdown("**Paleta de colores activa:**")
        st.markdown(
            f"""
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <div style="background:{cfg_inv.get('color_primario', '#00ffff')}; width:70px; height:40px; border-radius:8px; border:1px solid #ccc;"></div>
                <div style="background:{cfg_inv.get('color_secundario', '#ff00ff')}; width:70px; height:40px; border-radius:8px; border:1px solid #ccc;"></div>
                <div style="background:{cfg_inv.get('color_fondo', '#060e1d')}; width:70px; height:40px; border-radius:8px; border:1px solid #ccc;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("**Disco / Audio activo:**")
        prev_audio = obtener_vista_previa(cfg_inv.get("audio_url"))
        if prev_audio:
            st.audio(prev_audio)
        else:
            st.info("Usando el audio local por defecto (`musica.mp3`).")