import streamlit as st
import requests, json
API = st.secrets["API_URL"]   
st.title("Demo CRUD • DynamoDB + Lambda")
st.subheader("Crear nuevo registro")
with st.form("add"):
    name   = st.text_input("Nombre")
    edad   = st.number_input("Edad", min_value=0, step=1)
    comida = st.text_input("Comida favorita")
    submitted = st.form_submit_button("Guardar")
    if submitted and name and comida:
        resp = requests.post(f"{API}/items",
                             json={"name": name,
                                   "edad": int(edad),
                                   "comida_favorita": comida})
        if resp.status_code == 201:
            st.success("✅ Registro creado")
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
st.divider()
st.subheader("Registros")
data = requests.get(f"{API}/items").json()
if data:
    st.table(data)
else:
    st.info("No hay registros aún.")
    