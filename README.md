
# Verificador de Zonas Peligrosas en Guayaquil

Esta app en Streamlit permite ingresar coordenadas (latitud/longitud) y verificar si una ubicación cae dentro de una zona clasificada como peligrosa (roja, amarilla o verde) usando análisis espacial con GeoPandas y un mapa interactivo con Folium.

## ¿Cómo usar en Streamlit Cloud?

1. Sube este proyecto a un repositorio de GitHub.
2. Ve a https://streamlit.io/cloud e inicia sesión.
3. Haz clic en "New app", elige tu repositorio y despliega.
4. Asegúrate que el archivo principal sea: `app_zonas_guayaquil.py`.

## Archivos

- `app_zonas_guayaquil.py`: Código principal de la app.
- `zonas_peligrosas_guayaquil.geojson`: Capa simulada de zonas peligrosas.
- `requirements.txt`: Lista de dependencias para instalar en la nube.
