import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
SUPABASE_URL = "https://auezltquejptsupqkcqh.supabase.co"
SUPABASE_KEY = "sb_publishable_eImPwr3l_Wq-TO3FW4wk2g_YUCE898x"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de la página
st.set_page_config(page_title="Panel VIP - Pool Party", layout="centered")

st.title("📋 Panel de Control - Pool Party")
st.markdown("Aquí puedes ver quiénes han confirmado asistencia en tiempo real.")

# Botón para recargar los datos manualmente si lo deseas
if st.button("🔄 Actualizar Datos"):
    st.rerun()

# Consultar los datos a Supabase
try:
    respuesta = supabase.table("invitados_pool_party").select("*").execute()
    datos = respuesta.data
    
    if datos:
        # Convertir a DataFrame (Tabla)
        df = pd.DataFrame(datos)
        
        # Mostrar un contador gigante con el total de invitados
        st.metric(label="Total de Invitados Confirmados", value=len(df))
        
        # Ocultar la columna de ID u otras cosas técnicas si existen, para que se vea más limpio
        if 'id' in df.columns:
            df = df.drop(columns=['id'])
            
        # Mostrar la tabla con los datos
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("Aún no hay invitados registrados. ¡Comparte la invitación!")
        
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")