
import streamlit as st
import geopandas as gpd
import requests
import pandas as pd
import folium
from shapely.geometry import Point
from streamlit_folium import st_folium
import os
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📍 Verificador de Clientes en Zonas Peligrosas")

st.markdown("🔎 Coloca el **ID del cliente (1 a 1000)** o valida con **coordenadas nuevas**.")

clientes = gpd.read_file("clientes_1000_guayaquil.geojson")
kobo_token = os.getenv("KOBO_TOKEN")
form_id = "aqY6oRXU7iELs6bmj3VuwB"

@st.cache_data(ttl=60)
def get_zonas(token, form_id):
    headers = {"Authorization": f"Token {token}"}
    url = f"https://kf.kobotoolbox.org/api/v2/assets/{form_id}/data.geojson"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return gpd.read_file(BytesIO(response.content))
        except Exception as e:
            st.error(f"Error leyendo zonas: {e}")
            return None
    else:
        st.error(f"Error al conectarse a KoBo: {response.status_code}")
        return None

zonas = get_zonas(kobo_token, form_id) if kobo_token else None

# Inicializar session state
if "mensaje" not in st.session_state:
    st.session_state.mensaje = ""
if "punto" not in st.session_state:
    st.session_state.punto = None
if "cliente" not in st.session_state:
    st.session_state.cliente = None

with st.sidebar:
    st.header("🧭 Búsqueda")
    cliente_id = st.number_input("ID del cliente (1-1000)", min_value=1, max_value=1000, step=1)
    st.markdown("---")
    st.markdown("O coloca coordenadas:")
    lat_input = st.text_input("Latitud")
    lon_input = st.text_input("Longitud")
    buscar_btn = st.button("🔍 Buscar ubicación")

if buscar_btn:
    st.session_state.mensaje = ""
    st.session_state.punto = None
    st.session_state.cliente = None

    if lat_input and lon_input:
        try:
            lat = float(lat_input)
            lon = float(lon_input)
            punto = Point(lon, lat)
            riesgo = any(z.contains(punto) for z in zonas.geometry) if zonas is not None else False
            st.session_state.punto = punto
            st.session_state.mensaje = (
                "🛑 Esta ubicación está en una zona peligrosa. Se recomienda no realizar visitas en campo."
                if riesgo else
                "✅ Ubicación segura. Se puede programar una visita."
            )
        except:
            st.session_state.mensaje = "⚠️ Coordenadas inválidas"
    else:
        cliente_row = clientes[clientes["id_cliente"] == cliente_id]
        if not cliente_row.empty:
            punto = cliente_row.geometry.values[0]
            riesgo = any(z.contains(punto) for z in zonas.geometry) if zonas is not None else False
            st.session_state.punto = punto
            st.session_state.cliente = cliente_row.iloc[0]
            st.session_state.mensaje = (
                "🛑 El cliente está en una zona peligrosa. Se recomienda contactar por otros medios."
                if riesgo else
                "✅ Cliente en zona segura. Se puede visitar presencialmente."
            )
        else:
            st.session_state.mensaje = "❌ Cliente no encontrado"

# Mapa
m = folium.Map(location=[-2.2, -79.9], zoom_start=12)
folium.TileLayer("CartoDB positron").add_to(m)

if zonas is not None:
    for _, zona in zonas.iterrows():
        folium.GeoJson(zona.geometry, tooltip=zona.get("grupo_zona/nombre_zona", "Zona")).add_to(m)

if st.session_state.punto:
    folium.Marker(
        location=[st.session_state.punto.y, st.session_state.punto.x],
        icon=folium.Icon(color="blue", icon="info-sign"),
        popup=st.session_state.mensaje
    ).add_to(m)

st.subheader("🗺️ Mapa Interactivo")
st_folium(m, width=1000, height=600)

if st.session_state.mensaje:
    if "✅" in st.session_state.mensaje:
        st.success(st.session_state.mensaje)
    elif "🛑" in st.session_state.mensaje:
        st.error(st.session_state.mensaje)
    else:
        st.warning(st.session_state.mensaje)

if st.session_state.cliente is not None:
    st.markdown("### 🧾 Datos del Cliente")
    st.json(st.session_state.cliente.to_dict())
