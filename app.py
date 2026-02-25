import streamlit as st

st.set_page_config(page_title="THE DROP: 15 SALVADOR", layout="centered")

# Estilo Neón
st.markdown("<style>.stApp {background-color: #0e1117; color: #00f2ff;}</style>", unsafe_allow_html=True)

st.title("THE DROP: 15 // SALVADOR")

# Mostramos la invitación que tienes en tu GitHub
try:
    st.image("invitacion_neon.jpg", use_container_width=True)
except:
    st.error("Asegúrate de que el archivo se llame invitacion_neon.jpg en tu GitHub")

st.write("### FECHA: 25 DE ABRIL, 2026")
st.success("¡El servidor está vivo!")