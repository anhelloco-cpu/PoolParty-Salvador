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
st.markdown("Gestión de invitados y limpieza de duplicados en tiempo real.")

# --- FUNCIÓN PARA ELIMINAR DUPLICADOS ---
def eliminar_duplicados(df):
    # Identificar duplicados basados en Nombre y Apellido (ignorando mayúsculas/minúsculas)
    df['full_name_lower'] = (df['nombre'].str.strip() + " " + df['apellido'].str.strip()).str.lower()
    
    # Nos quedamos con el primer ID de cada grupo y marcamos los demás para borrar
    duplicados = df[df.duplicated(subset=['full_name_lower'], keep='first')]
    
    ids_a_eliminar = duplicados['id'].tolist()
    
    exitos = 0
    errores = 0
    
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
        
        # Métricas principales
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total de Registros", value=len(df))
        
        # Detección de duplicados
        df_clean_check = df.copy()
        df_clean_check['nombre_completo'] = (df_clean_check['nombre'].str.strip() + " " + df_clean_check['apellido'].str.strip()).str.lower()
        conteo_duplicados = df_clean_check.duplicated(subset=['nombre_completo'], keep='first').sum()
        
        with col2:
            st.metric(label="Registros Repetidos", value=conteo_duplicados, delta_color="inverse")

        # --- SECCIÓN DE LIMPIEZA ---
        if conteo_duplicados > 0:
            st.warning(f"Se han detectado {conteo_duplicados} invitados repetidos (mismo nombre y apellido).")
            if st.button("🗑️ ELIMINAR REGISTROS REPETIDOS"):
                with st.spinner("Limpiando base de datos..."):
                    exitos, errores = eliminar_duplicados(df)
                    if exitos > 0:
                        st.success(f"¡Limpieza completada! Se eliminaron {exitos} registros duplicados.")
                        st.rerun()
                    if errores > 0:
                        st.error(f"No se pudieron eliminar {errores} registros. Revisa la conexión.")
        else:
            st.success("✅ No se encontraron registros duplicados.")

        # --- TABLA DE INVITADOS ---
        st.subheader("Lista Detallada")
        # Reordenar para que sea más legible
        columnas_visibles = ['nombre', 'apellido', 'gusto_comida', 'disco_preferido']
        # Solo mostrar columnas que existan en el DF
        columnas_finales = [c for c in columnas_visibles if c in df.columns]
        
        st.dataframe(df[columnas_finales].sort_values(by='nombre'), use_container_width=True)
        
        if st.button("🔄 Refrescar Lista"):
            st.rerun()
            
    else:
        st.info("Aún no hay invitados registrados.")
        if st.button("🔄 Verificar de nuevo"):
            st.rerun()
        
except Exception as e:
    st.error(f"Error al conectar con Supabase: {e}")