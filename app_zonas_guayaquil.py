
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Zonas Peligrosas - Guayaquil", layout="centered")

st.title("🧭 Verificador de Zonas Peligrosas en Guayaquil")

# Cargar zonas
zonas = gpd.read_file("zonas_peligrosas_guayaquil.geojson")

# Entrada de coordenadas
lat = st.number_input("Ingrese latitud:", value=-2.185, format="%.6f")
lon = st.number_input("Ingrese longitud:", value=-79.915, format="%.6f")

# Verificar zona
if st.button("Verificar ubicación"):
    punto = gpd.GeoDataFrame([{'geometry': Point(lon, lat)}], crs='EPSG:4326')
    resultado = gpd.sjoin(punto, zonas, how='left', predicate='intersects')

    if not resultado.empty:
        zona = resultado.iloc[0]['zona']
        tipo = resultado.iloc[0]['tipo']
        st.success(f"📍 Zona detectada: {zona} ({tipo})")
    else:
        st.warning("⚠️ La ubicación no se encuentra en una zona clasificada.")

    # Mostrar mapa
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.GeoJson("zonas_peligrosas_guayaquil.geojson", name="Zonas").add_to(m)
    folium.Marker([lat, lon], tooltip="Ubicación del cliente").add_to(m)
    folium_static(m)
