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
st.markdown("Gestión de invitados y limpieza de duplicados.")

# --- FUNCIÓN PARA ELIMINAR DUPLICADOS ---
def eliminar_duplicados(df):
    # Identificar duplicados basados en Nombre y Apellido
    df['nombre_completo'] = (df['nombre'].str.strip() + " " + df['apellido'].str.strip()).str.lower()
    
    # Nos quedamos con el primer ID de cada grupo y marcamos los demás para borrar
    duplicados_a_borrar = df[df.duplicated(subset=['nombre_completo'], keep='first')]
    
    ids_a_eliminar = duplicados_a_borrar['id'].tolist()
    
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
        
        # Preparar columna limpia para comparar
        df['nombre_completo'] = (df['nombre'].str.strip() + " " + df['apellido'].str.strip()).str.lower()
        
        # Contar cuántos son copias exactas que sobran
        conteo_sobrantes = df.duplicated(subset=['nombre_completo'], keep='first').sum()
        
        # --- MÉTRICAS ---
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total de Registros (Actual)", value=len(df))
        with col2:
            st.metric(label="Registros Repetidos (Sobrantes)", value=conteo_sobrantes, delta_color="inverse")

        st.divider()

        # --- SECCIÓN DE VISTA PREVIA Y LIMPIEZA ---
        if conteo_sobrantes > 0:
            st.warning(f"⚠️ Se han detectado {conteo_sobrantes} registros repetidos. Revisa la tabla de sospechosos a continuación:")
            
            # Filtrar el DataFrame para mostrar TODOS los registros que comparten nombre (originales y copias)
            # keep=False marca todos los elementos de los grupos duplicados
            df_mostrar_repetidos = df[df.duplicated(subset=['nombre_completo'], keep=False)].sort_values(by='nombre_completo')
            
            # Definir qué columnas mostrar en la vista previa
            columnas_revisar = ['nombre', 'apellido', 'gusto_comida', 'disco_preferido']
            if 'created_at' in df.columns:
                columnas_revisar.append('created_at') # Mostrar fecha si existe para ver cuál fue primero
                
            columnas_finales_rev = [c for c in columnas_revisar if c in df_mostrar_repetidos.columns]
            
            # Mostrar la tabla de sospechosos
            st.dataframe(df_mostrar_repetidos[columnas_finales_rev], use_container_width=True)
            
            st.info("💡 Nota: Si presionas eliminar, el sistema mantendrá el registro más antiguo de cada persona y borrará las copias.")
            
            # Botón de confirmación
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

        # --- TABLA GENERAL DE INVITADOS ---
        st.subheader("👥 Lista General de Invitados")
        
        # Ocultar columnas técnicas para la vista general
        columnas_visibles = ['nombre', 'apellido', 'gusto_comida', 'disco_preferido']
        columnas_finales = [c for c in columnas_visibles if c in df.columns]
        
        # Mostrar tabla ordenada alfabéticamente
        st.dataframe(df[columnas_finales].sort_values(by='nombre'), use_container_width=True)
        
        if st.button("🔄 Refrescar Lista General"):
            st.rerun()
            
    else:
        st.info("Aún no hay invitados registrados. ¡El rancho está vacío!")
        if st.button("🔄 Verificar de nuevo"):
            st.rerun()
        
except Exception as e:
    st.error(f"Error al conectar con Supabase: {e}")