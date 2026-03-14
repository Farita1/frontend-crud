import streamlit as st
import requests
import pandas as pd

API = st.secrets["API_URL"]   

st.title("Demo CRUD • DynamoDB + Lambda")

st.subheader("Crear nuevo registro")
with st.form("add"):
    name   = st.text_input("Nombre")
    # Aseguramos que el input sea entero con step=1
    edad   = st.number_input("Edad", min_value=0, step=1)
    comida = st.text_input("Comida favorita")
    submitted = st.form_submit_button("Guardar")
    
    if submitted and name and comida:
        resp = requests.post(
            f"{API}/items",
            json={
                "name": name,
                "edad": int(edad),
                "comida_favorita": comida
            }
        )
        if resp.status_code == 201:
            st.success("✅ Registro creado")
            st.rerun() # Opcional: recarga para ver el cambio de inmediato
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")

st.divider()

st.subheader("Registros")
response = requests.get(f"{API}/items")

if response.status_code == 200:
    data = response.json()
    if data:
        # Convertimos a DataFrame para manipular el formato
        df = pd.DataFrame(data)
        
        # Si la columna 'edad' existe, la convertimos a entero
        if 'edad' in df.columns:
            df['edad'] = df['edad'].astype(int)
        
        # Usamos st.dataframe o st.table con el DataFrame procesado
        st.table(df)
    else:
        st.info("No hay registros aún.")
else:
    st.error("No se pudo conectar con la API.")