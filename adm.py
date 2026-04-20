import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
from docx import Document

# --- CONFIGURACIÓN SUPABASE ---
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de la página
st.set_page_config(page_title="Panel VIP - Pool Party", layout="wide")

st.title("📋 Panel de Control Financiero - Pool Party")
st.markdown("Gestión de invitados y presupuesto profesional (Costos Fijos vs Variables).")

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

# --- CARGA DE DATOS ---
try:
    respuesta = supabase.table("invitados_pool_party").select("*").execute()
    datos = respuesta.data
    
    if datos:
        df = pd.DataFrame(datos)
        
        # Crear pestañas
        tab1, tab2 = st.tabs(["👥 Gestión de Invitados", "📊 Presupuesto Profesional"])
        
        # ==========================================
        # PESTAÑA 1: GESTIÓN DE INVITADOS
        # ==========================================
        with tab1:
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
                if 'created_at' in df.columns: columnas_revisar.append('created_at')
                
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
            if st.button("🔄 Refrescar Lista"): st.rerun()

        # ==========================================
        # PESTAÑA 2: CALCULADORA PROFESIONAL
        # ==========================================
        with tab2:
            st.header("Estructura de Costos")
            
            # Contar preferencias reales
            conteo_comida = df['gusto_comida'].value_counts()
            total_carne = conteo_comida.get('Carne', 0) + conteo_comida.get('Sin preferencia', 0)
            total_pollo = conteo_comida.get('Pollo', 0)
            total_vege = conteo_comida.get('Vegetariano', 0)
            total_invitados = len(df)
            
            st.info(f"**Invitados Confirmados:** {total_carne} Carne | {total_pollo} Pollo | {total_vege} Veggie | **Total: {total_invitados} personas**")

            with st.form("form_presupuesto"):
                
                st.subheader("📈 COSTOS VARIABLES (Dependen del # de invitados)")
                col_c1, col_c2 = st.columns(2)
                precio_carne = col_c1.number_input("Precio por Kilo Carne ($)", value=35000)
                gr_carne = col_c2.number_input("Gramos carne por persona", value=350)
                
                col_p1, col_p2 = st.columns(2)
                precio_pollo = col_p1.number_input("Precio por Kilo Pollo ($)", value=18000)
                gr_pollo = col_p2.number_input("Gramos pollo por persona", value=350)
                
                st.markdown("---")
                st.write("**Pasabocas y Acompañamientos**")
                nombre_pasa = st.text_input("Tipo de Pasabocas", value="Deditos y empanaditas")
                col_b1, col_b2, col_b3 = st.columns(3)
                precio_unid_pasa = col_b1.number_input("Precio Unidad Pasaboca ($)", value=1200)
                unid_persona_ronda = col_b2.number_input("Und. por persona (por ronda)", value=4)
                num_rondas = col_b3.number_input("Número de rondas", value=2)
                
                col_a1, col_a2 = st.columns(2)
                costo_acompa = col_a1.number_input("Acompañamientos p/p ($) (Yuca, papa, etc.)", value=6000)
                presu_bebidas = col_a2.number_input("Presupuesto Bebidas e Hielo ($)", value=250000)
                
                st.divider()

                st.subheader("📌 COSTOS FIJOS (Independientes de la asistencia)")
                col_f1, col_f2 = st.columns(2)
                costo_lugar = col_f1.number_input("Alquiler del Lugar / Rancho JP ($)", value=500000, step=50000)
                costo_dj = col_f2.number_input("DJ Calao y Sonido ($)", value=250000, step=10000)
                
                costo_deco = st.number_input("Decoración Neón y Ambientación ($)", value=100000, step=10000)
                
                st.divider()
                margen = st.slider("Margen Financiero para Imprevistos (%)", 0, 20, 10)
                
                generar = st.form_submit_button("💰 GENERAR INFORME FINANCIERO")

            if generar:
                # ================= MATEMÁTICAS =================
                # Costos Variables
                k_carne = (total_carne * gr_carne) / 1000
                gasto_carne = k_carne * precio_carne
                k_pollo = (total_pollo * gr_pollo) / 1000
                gasto_pollo = k_pollo * precio_pollo
                
                total_unidades_pasa = total_invitados * unid_persona_ronda * num_rondas
                gasto_pasabocas = total_unidades_pasa * precio_unid_pasa
                gasto_acompa = total_invitados * costo_acompa
                
                total_variables = gasto_carne + gasto_pollo + gasto_pasabocas + gasto_acompa + presu_bebidas
                
                # Costos Fijos
                total_fijos = costo_lugar + costo_dj + costo_deco
                
                # Totales Generales
                subtotal = total_variables + total_fijos
                monto_imprevistos = subtotal * (margen / 100)
                gran_total = subtotal + monto_imprevistos
                
                cuota_por_persona = gran_total / total_invitados if total_invitados > 0 else 0
                
                # ================= INTERFAZ DE RESULTADOS =================
                st.divider()
                st.subheader("📊 Resumen Ejecutivo")
                
                r1, r2, r3, r4 = st.columns(4)
                r1.metric("Kilos Carne", f"{k_carne:.1f} kg")
                r2.metric("Kilos Pollo", f"{k_pollo:.1f} kg")
                r3.metric("Total Pasabocas", f"{total_unidades_pasa} und")
                r4.metric("Cuota Est. p/p", f"${cuota_por_persona:,.0f}")

                # ================= TICKET PROFESIONAL =================
                resumen_print = f"""
                ### 📝 REPORTE FINANCIERO: POOL PARTY SALVADOR
                ---
                **Asistencia Proyectada:** {total_invitados} personas
                
                **1. COSTOS VARIABLES:**
                * Proteína (Carne {k_carne:.1f}kg + Pollo {k_pollo:.1f}kg): **${(gasto_carne + gasto_pollo):,.0f}**
                * Pasabocas ({nombre_pasa} - {total_unidades_pasa} unds): **${gasto_pasabocas:,.0f}**
                * Acompañamientos: **${gasto_acompa:,.0f}**
                * Bebidas e Hielo: **${presu_bebidas:,.0f}**
                * **Subtotal Variables: ${total_variables:,.0f}**
                
                **2. COSTOS FIJOS:**
                * Alquiler de Locación (Rancho JP): **${costo_lugar:,.0f}**
                * DJ Calao y Sistema de Sonido: **${costo_dj:,.0f}**
                * Decoración Neón y Ambientación: **${costo_deco:,.0f}**
                * **Subtotal Fijos: ${total_fijos:,.0f}**
                
                **3. CONSOLIDADO:**
                * Subtotal Operativo: ${subtotal:,.0f}
                * Fondo de Imprevistos ({margen}%): ${monto_imprevistos:,.0f}
                
                ### **VALOR TOTAL DEL PROYECTO: ${gran_total:,.0f}**
                
                ---
                *Punto de equilibrio (Cuota sugerida por invitado): ${cuota_por_persona:,.0f}*
                """
                st.markdown(resumen_print)
                
                # BOTÓN DE IMPRESIÓN 
                st.button("🖨️ PREPARAR PARA IMPRIMIR (Ctrl + P)", on_click=lambda: st.info("Usa Ctrl + P (o Cmd + P en Mac) para guardar este reporte en PDF o imprimirlo."))

                # ====================================================================
                # NUEVA SECCIÓN DE EXPORTACIÓN Y GUARDADO (CON FILTRO DE EMOJIS)
                # ====================================================================
                st.divider()
                st.subheader("💾 Opciones de Exportación")
                col_d1, col_d2, col_d3 = st.columns(3)

                # 1. GENERAR PDF EN MEMORIA (A prueba de errores)
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                for linea in resumen_print.split('\n'):
                    # Limpiamos el markdown y los asteriscos
                    texto_limpio = linea.replace('**', '').replace('### ', '').replace('---', '-'*50).replace('📝', '').strip()
                    
                    # MAGIA AQUÍ: Forzamos el texto a Latin-1 para eliminar los emojis invisibles y evitar que se estrelle
                    texto_limpio = texto_limpio.encode('latin-1', 'ignore').decode('latin-1')
                    
                    if texto_limpio:
                        pdf.cell(0, 7, txt=texto_limpio, ln=True)
                
                # Guardado compatible con cualquier versión de FPDF
                try:
                    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                except AttributeError:
                    pdf_bytes = bytes(pdf.output())

                col_d1.download_button(
                    label="📄 Descargar como PDF", 
                    data=pdf_bytes, 
                    file_name="Presupuesto_PoolParty.pdf", 
                    mime="application/pdf"
                )

                # 2. GENERAR WORD EN MEMORIA
                doc = Document()
                doc.add_heading('Reporte Financiero Pool Party', 0)
                for linea in resumen_print.split('\n'):
                    texto_limpio = linea.replace('**', '').replace('### ', '').replace('---', '-'*50).replace('📝', '').strip()
                    if texto_limpio:
                        doc.add_paragraph(texto_limpio)
                b = BytesIO()
                doc.save(b)
                word_bytes = b.getvalue()

                col_d2.download_button(
                    label="📝 Descargar como Word", 
                    data=word_bytes, 
                    file_name="Presupuesto_PoolParty.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

                # 3. GUARDAR EN SUPABASE
                datos_guardar = {
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_invitados": total_invitados,
                    "costos_variables": float(total_variables),
                    "costos_fijos": float(total_fijos),
                    "gran_total": float(gran_total),
                    "cuota_por_persona": float(cuota_por_persona)
                }

                if col_d3.button("☁️ Guardar Presupuesto"):
                    try:
                        supabase.table("presupuestos_historicos").insert(datos_guardar).execute()
                        st.success("✅ ¡Presupuesto guardado exitosamente en tu base de datos!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"⚠️ Error al guardar. Verifica que creaste la tabla 'presupuestos_historicos' en Supabase. Detalle: {e}")

    else:
        st.info("Aún no hay invitados registrados en la base de datos.")
        if st.button("🔄 Reintentar"): st.rerun()
        
except Exception as e:
    st.error(f"Error de conexión: {e}")