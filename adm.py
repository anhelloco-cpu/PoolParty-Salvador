import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de la página
st.set_page_config(page_title="Panel VIP - Pool Party", layout="wide")

st.title("📋 Panel de Control - Pool Party")
st.markdown("Gestión de invitados y calculadora de presupuesto automático.")

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
        
        # Crear pestañas para organizar el panel
        tab1, tab2 = st.tabs(["👥 Gestión de Invitados", "💰 Calculadora de Presupuesto"])
        
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
        # PESTAÑA 2: CALCULADORA DE PRESUPUESTO
        # ==========================================
        with tab2:
            st.header("Generador de Presupuesto Automático")
            
            conteo_comida = df['gusto_comida'].value_counts()
            total_carne = conteo_comida.get('Carne', 0) + conteo_comida.get('Sin preferencia', 0)
            total_pollo = conteo_comida.get('Pollo', 0)
            total_vege = conteo_comida.get('Vegetariano', 0)
            total_invitados = len(df)
            
            st.info(f"**Invitados Confirmados:** {total_invitados}")

            with st.form("form_presupuesto"):
                st.subheader("🥩 Plato Principal (Proteína)")
                c1, c2 = st.columns(2)
                precio_carne = c1.number_input("Precio por Kilo Carne ($)", value=35000)
                gr_carne = c2.number_input("Gramos carne por persona", value=350)
                
                c3, c4 = st.columns(2)
                precio_pollo = c3.number_input("Precio por Kilo Pollo ($)", value=18000)
                gr_pollo = c4.number_input("Gramos pollo por persona", value=350)
                
                # SECCIÓN DE PASABOCAS INGENIADA
                st.subheader("🥟 Sección de Pasabocas")
                nombre_pasa = st.text_input("¿Qué pasabocas darás?", value="Deditos y empanaditas")
                col_p1, col_p2, col_p3 = st.columns(3)
                precio_unid_pasa = col_p1.number_input("Precio por UNIDAD ($)", value=1200)
                unid_persona_ronda = col_p2.number_input("Unidades por persona (en cada ronda)", value=4)
                num_rondas = col_p3.number_input("¿Cuántas veces repartirás?", value=2)
                
                st.subheader("🥗 Otros y Decoración")
                col_e1, col_e2 = st.columns(2)
                costo_acompa = col_e1.number_input("Acompañamientos p/p ($)", value=6000)
                costo_deco = col_e2.number_input("Presupuesto Decoración Neón ($)", value=100000)
                
                col_l1, col_l2 = st.columns(2)
                presu_bebidas = col_l1.number_input("Presupuesto Bebidas/Hielo ($)", value=250000)
                costo_dj = col_l2.number_input("DJ Calao y Logística ($)", value=250000)
                
                margen = st.slider("Margen de Imprevistos (%)", 0, 20, 10)
                
                generar = st.form_submit_button("💰 CALCULAR PRESUPUESTO")

            if generar:
                # CÁLCULOS PROTEÍNA
                k_carne = (total_carne * gr_carne) / 1000
                gasto_carne = k_carne * precio_carne
                k_pollo = (total_pollo * gr_pollo) / 1000
                gasto_pollo = k_pollo * precio_pollo
                
                # CÁLCULOS PASABOCAS
                total_unidades_pasa = total_invitados * unid_persona_ronda * num_rondas
                gasto_pasabocas = total_unidades_pasa * precio_unid_pasa
                
                # TOTALES
                gasto_acompa = total_invitados * costo_acompa
                subtotal = gasto_carne + gasto_pollo + gasto_pasabocas + gasto_acompa + presu_bebidas + costo_dj + costo_deco
                total_final = subtotal * (1 + (margen/100))
                cuota = total_final / total_invitados if total_invitados > 0 else 0
                
                st.divider()
                st.subheader("📊 Resumen de Inversión")
                
                r1, r2, r3, r4 = st.columns(4)
                r1.metric("Kilos Carne", f"{k_carne:.1f} kg")
                r2.metric("Kilos Pollo", f"{k_pollo:.1f} kg")
                r3.metric("Total Pasabocas", f"{total_unidades_pasa} und")
                r4.metric("Cuota p/p", f"${cuota:,.0f}")

                # ÁREA DE IMPRESIÓN (Formato limpio)
                resumen_print = f"""
                ### 📝 PRESUPUESTO: POOL PARTY SALVADOR
                ---
                **Invitados Confirmados:** {total_invitados}
                
                **1. COMIDA PRINCIPAL:**
                * Carne ({k_carne:.1f} kg): ${gasto_carne:,.0f}
                * Pollo ({k_pollo:.1f} kg): ${gasto_pollo:,.0f}
                * Acompañamientos: ${gasto_acompa:,.0f}
                
                **2. PASABOCAS ({nombre_pasa}):**
                * Cantidad total: {total_unidades_pasa} unidades
                * Detalle: {unid_persona_ronda} p/p x {num_rondas} rondas.
                * Inversión pasabocas: ${gasto_pasabocas:,.0f}
                
                **3. LOGÍSTICA Y DECO:**
                * Decoración: ${costo_deco:,.0f}
                * Bebidas e Hielo: ${presu_bebidas:,.0f}
                * DJ Calao y Sonido: ${costo_dj:,.0f}
                
                **4. TOTALES:**
                * Subtotal: ${subtotal:,.0f}
                * Imprevistos ({margen}%): ${(total_final - subtotal):,.0f}
                * **VALOR TOTAL ESTIMADO: ${total_final:,.0f}**
                
                ---
                *Promedio por invitado: ${cuota:,.0f}*
                """
                st.markdown(resumen_print)
                
                # BOTÓN DE IMPRESIÓN (Simulado para que el usuario use Ctrl+P o copie)
                st.button("🖨️ CLIC AQUÍ PARA PREPARAR IMPRESIÓN", on_click=lambda: st.info("Usa Ctrl + P en tu teclado para imprimir este resumen ahora."))

    else:
        st.info("Aún no hay invitados registrados.")
        if st.button("🔄 Reintentar"): st.rerun()
        
except Exception as e:
    st.error(f"Error de conexión: {e}")