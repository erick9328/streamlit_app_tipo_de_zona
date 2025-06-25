
import streamlit as st
import geopandas as gpd
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from shapely.geometry import shape, Point
import os

st.set_page_config(layout="wide")
st.title("🛰️ Visor de Clientes en Zonas Peligrosas con Recomendación")

# Cargar clientes desde archivo GeoJSON local
clientes = gpd.read_file("clientes_fibra_guayaquil.geojson")

# Token seguro desde secrets
kobo_token = os.getenv("KOBO_TOKEN")

# ID del formulario (puede seguir siendo editable si lo necesitas)
st.sidebar.header("🧾 Configuración del Formulario")
form_id = st.sidebar.text_input("ID del formulario KoBo", value="aqY6oRXU7iELs6bmj3VuwB")

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
        clientes["en_zona_peligrosa"] = clientes.geometry.apply(
            lambda punto: any(polygon.contains(punto) for polygon in zonas.geometry)
        )

        st.sidebar.header("🔎 Búsqueda Manual")
        cliente_id = st.sidebar.number_input("Buscar por ID de cliente", min_value=1, max_value=2000, step=1)
        buscar_coords = st.sidebar.checkbox("Buscar por coordenadas")
        lat_input = st.sidebar.text_input("Latitud")
        lon_input = st.sidebar.text_input("Longitud")

        punto_focal = None
        mensaje = ""

        if st.sidebar.button("Buscar"):
            if buscar_coords and lat_input and lon_input:
                try:
                    lat = float(lat_input)
                    lon = float(lon_input)
                    punto_focal = Point(lon, lat)
                    riesgo = any(polygon.contains(punto_focal) for polygon in zonas.geometry)
                    mensaje = "🛑 Zona peligrosa - evitar visita" if riesgo else "✅ Seguro - se puede visitar"
                except:
                    mensaje = "⚠️ Coordenadas inválidas"
            else:
                cliente_row = clientes[clientes["id_cliente"] == cliente_id]
                if not cliente_row.empty:
                    punto_focal = cliente_row.geometry.values[0]
                    riesgo = cliente_row["en_zona_peligrosa"].values[0]
                    mensaje = "🛑 Zona peligrosa - evitar visita" if riesgo else "✅ Seguro - se puede visitar"
                else:
                    mensaje = "❌ Cliente no encontrado"

        m = folium.Map(location=[-2.2, -79.9], zoom_start=12)
        folium.TileLayer("CartoDB positron").add_to(m)

        for _, zona in zonas.iterrows():
            folium.GeoJson(zona.geometry, tooltip=zona.get("grupo_zona/nombre_zona", "Zona")).add_to(m)

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

        if punto_focal:
            folium.Marker(
                location=[punto_focal.y, punto_focal.x],
                icon=folium.Icon(color="blue", icon="info-sign"),
                popup=mensaje
            ).add_to(m)

        st.subheader("🗺️ Mapa Interactivo")
        st_folium(m, width=1000, height=600)

        if mensaje:
            st.success(mensaje) if "✅" in mensaje else st.warning(mensaje)

        en_riesgo = clientes[clientes["en_zona_peligrosa"]]
        st.markdown(f"### ⚠️ Clientes en zona peligrosa: {len(en_riesgo)}")
        st.dataframe(en_riesgo[["id_cliente", "nombre", "lat", "lon"]])
    else:
        st.warning("No se encontraron zonas peligrosas.")
else:
    st.info("El token de KoBo no está configurado como secreto. Agrégalo como KOBO_TOKEN en Streamlit Cloud.")
