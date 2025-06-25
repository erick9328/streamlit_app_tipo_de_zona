
import streamlit as st
import geopandas as gpd
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from shapely.geometry import shape

st.set_page_config(layout="wide")
st.title("🛰️ Visor de Clientes en Zonas Peligrosas")

# 1. Cargar clientes desde archivo GeoJSON local
clientes = gpd.read_file("clientes_fibra_guayaquil.geojson")

# 2. Cargar zonas peligrosas desde la API de KoBoToolbox
st.sidebar.header("🔐 API KoBo")
kobo_token = st.sidebar.text_input("Token de KoBo (privado)", type="password")
kobo_url = "https://kf.kobotoolbox.org/api/v2/assets/"

# ID del formulario que contiene los polígonos de zonas peligrosas
form_id = st.sidebar.text_input("ID del formulario", value="aqY6oRXU7iELs6bmj3VuwB")

@st.cache_data(ttl=60)
def get_geojson_from_kobo(token, form_id):
    headers = {"Authorization": f"Token {token}"}
    geojson_url = f"https://kf.kobotoolbox.org/api/v2/assets/{form_id}/data.geojson"
    response = requests.get(geojson_url, headers=headers)
    if response.status_code == 200:
        gdf = gpd.read_file(response.text)
        return gdf
    else:
        st.error(f"Error al obtener GeoJSON: {response.status_code}")
        return None

if kobo_token and form_id:
    zonas = get_geojson_from_kobo(kobo_token, form_id)

    if zonas is not None and not zonas.empty:
        # 3. Cruce espacial: clientes que caen en zonas peligrosas
        clientes["en_zona_peligrosa"] = clientes.geometry.apply(
            lambda punto: any(polygon.contains(punto) for polygon in zonas.geometry)
        )

        # 4. Visualización
        m = folium.Map(location=[-2.2, -79.9], zoom_start=12)
        folium.TileLayer("CartoDB positron").add_to(m)

        # Zonas peligrosas
        for _, zona in zonas.iterrows():
            folium.GeoJson(zona.geometry, tooltip=zona.get("grupo_zona/nombre_zona", "Zona")).add_to(m)

        # Clientes
        for _, row in clientes.iterrows():
            color = "red" if row["en_zona_peligrosa"] else "green"
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=4,
                color=color,
                fill=True,
                fill_opacity=0.7,
                tooltip=row["nombre"]
            ).add_to(m)

        st.subheader("🗺️ Mapa Interactivo")
        st_folium(m, width=1000, height=600)

        # 5. Mostrar sugerencias
        en_riesgo = clientes[clientes["en_zona_peligrosa"]]
        st.markdown(f"### ⚠️ Clientes en zona peligrosa: {len(en_riesgo)}")

        if not en_riesgo.empty:
            st.dataframe(en_riesgo[["id_cliente", "nombre", "lat", "lon"]])
    else:
        st.warning("No se encontraron zonas peligrosas.")
else:
    st.info("Ingresa tu token de KoBo y el ID del formulario para comenzar.")
