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
        # PESTAÑA 1: GESTIÓN DE INVITADOS (Tu código anterior)
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
            st.markdown("El sistema lee tus invitados y calcula lo que necesitas comprar.")
            
            # Contar preferencias reales de la base de datos
            conteo_comida = df['gusto_comida'].value_counts()
            num_carne = conteo_comida.get('Carne', 0)
            num_pollo = conteo_comida.get('Pollo', 0)
            num_vege = conteo_comida.get('Vegetariano', 0)
            num_sin_pref = conteo_comida.get('Sin preferencia', 0)
            
            # Para presupuestar, asumimos que los "Sin preferencia" comen Carne (para ir seguros)
            total_carne = num_carne + num_sin_pref
            total_pollo = num_pollo
            total_vege = num_vege
            total_invitados = len(df)
            
            st.info(f"**Resumen de Platos:** {total_carne} Carne/Sin pref. | {total_pollo} Pollo | {total_vege} Vegetarianos | **Total: {total_invitados} pers.**")
            
            with st.form("form_presupuesto"):
                st.subheader("🥩 Insumos Directos (Proteína)")
                col_c1, col_c2 = st.columns(2)
                precio_carne = col_c1.number_input("Precio por Kilo de Carne ($)", value=35000, step=1000)
                gr_carne = col_c2.number_input("Gramos de carne por persona", value=350, step=50)
                
                col_p1, col_p2 = st.columns(2)
                precio_pollo = col_p1.number_input("Precio por Kilo de Pollo ($)", value=15000, step=1000)
                gr_pollo = col_p2.number_input("Gramos de pollo por persona", value=350, step=50)
                
                precio_vege = st.number_input("Presupuesto por plato Vegetariano ($)", value=12000, step=1000)
                
                st.subheader("🥗 Extras y Logística")
                col_e1, col_e2 = st.columns(2)
                costo_acompañamientos = col_e1.number_input("Acompañamientos por persona ($) (Yuca, papa, ensalada...)", value=5000, step=500)
                presupuesto_bebidas = col_e2.number_input("Presupuesto Total Bebidas e Hielo ($)", value=150000, step=10000)
                
                col_l1, col_l2 = st.columns(2)
                costo_lugar = col_l1.number_input("Costo del Lugar / Rancho JP ($)", value=0, step=50000)
                costo_dj = col_l2.number_input("Costo DJ Calao y Sonido ($)", value=200000, step=10000)
                
                imprevistos_pct = st.slider("Margen para Imprevistos/Desechables (%)", min_value=0, max_value=30, value=10)
                
                calcular = st.form_submit_button("💰 GENERAR PRESUPUESTO", use_container_width=True)
                
            if calcular:
                st.divider()
                st.subheader("📊 Resultados del Presupuesto")
                
                # MATEMÁTICAS
                kilos_carne = (total_carne * gr_carne) / 1000
                total_gasto_carne = kilos_carne * precio_carne
                
                kilos_pollo = (total_pollo * gr_pollo) / 1000
                total_gasto_pollo = kilos_pollo * precio_pollo
                
                total_gasto_vege = total_vege * precio_vege
                
                gasto_acompañamientos = total_invitados * costo_acompañamientos
                
                subtotal_comida = total_gasto_carne + total_gasto_pollo + total_gasto_vege + gasto_acompañamientos
                subtotal_logistica = presupuesto_bebidas + costo_lugar + costo_dj
                
                subtotal_general = subtotal_comida + subtotal_logistica
                monto_imprevistos = subtotal_general * (imprevistos_pct / 100)
                
                gran_total = subtotal_general + monto_imprevistos
                
                costo_por_cabeza = gran_total / total_invitados if total_invitados > 0 else 0
                
                # MOSTRAR RESULTADOS
                col_r1, col_r2, col_r3 = st.columns(3)
                col_r1.metric("Total Carne a Comprar", f"{kilos_carne:.1f} Kg")
                col_r2.metric("Total Pollo a Comprar", f"{kilos_pollo:.1f} Kg")
                col_r3.metric("Costo por Invitado", f"${costo_por_cabeza:,.0f}")
                
                st.write("")
                st.markdown(f"""
                **Desglose de Costos:**
                * 🥩 Gasto en Carne: **${total_gasto_carne:,.0f}**
                * 🍗 Gasto en Pollo: **${total_gasto_pollo:,.0f}**
                * 🥗 Gasto Vegetarianos: **${total_gasto_vege:,.0f}**
                * 🥔 Acompañamientos: **${gasto_acompañamientos:,.0f}**
                * 🍻 Bebidas e Hielo: **${presupuesto_bebidas:,.0f}**
                * 🎧 Lugar y DJ: **${(costo_lugar + costo_dj):,.0f}**
                * 💸 Imprevistos ({imprevistos_pct}%): **${monto_imprevistos:,.0f}**
                """)
                
                st.error(f"### GRAN TOTAL ESTIMADO: ${gran_total:,.0f}")

    else:
        st.info("Aún no hay invitados registrados. ¡El rancho está vacío!")
        if st.button("🔄 Verificar de nuevo"): st.rerun()
        
except Exception as e:
    st.error(f"Error al conectar con Supabase: {e}")