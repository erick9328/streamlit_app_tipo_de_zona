
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🗺️ Zonas Peligrosas desde KoBoToolbox")
st.markdown("Este visor carga en tiempo real los datos del formulario en KoBoToolbox de forma segura usando tu token de acceso.")

# Token y Asset ID
import os
token = os.getenv("KOBO_TOKEN")
asset_uid = "aqY6oRXU7iELs6bmj3VuwB"
url = f"https://kc.kobotoolbox.org/api/v2/assets/{asset_uid}/data.geojson"

# Petición con autenticación
headers = {"Authorization": f"Token {token}"}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    st.error("Error al conectar con KoBoToolbox. Revisa el token o el ID del formulario.")
else:
    geojson_data = response.json()

    # Crear mapa centrado en Guayaquil
    m = folium.Map(location=[-2.2, -79.9], zoom_start=12, tiles="cartodbpositron")

    # Cargar zonas peligrosas
    folium.GeoJson(
        geojson_data,
        name="Zonas peligrosas",
        tooltip=folium.GeoJsonTooltip(
            fields=["grupo_zona/nombre_zona", "grupo_zona/tipo_riesgo", "grupo_zona/observaciones"],
            aliases=["Zona:", "Riesgo:", "Observaciones:"],
            sticky=False
        )
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st_data = st_folium(m, width=1200, height=700)
