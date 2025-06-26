# 🛰️ Verificador de Clientes en Zonas Peligrosas (GeoAnalytics)

Este proyecto incluye dos opciones para validar si un cliente (con ubicación) se encuentra en una zona peligrosa definida por usuarios en campo (vía KoBoCollect):

- ✔️ **Streamlit App:** Visor web interactivo, rápido para usuarios finales.
- ✔️ **Notebook en Colab/Jupyter:** Análisis geoespacial detallado y exportación de resultados.

---

## 🗂️ Archivos principales

- `visor_clientes_zonas_peligrosas.py` – Aplicación Streamlit lista para subir a la nube o servidor.
- `Verificador de Clientes en Zonas Peligrosas (GeoPandas + KoBoToolbox).ipynb` – Notebook para Google Colab o JupyterLab,  incluye mapas y cruces.
- `clientes_1000_guayaquil.geojson` – Muestra de 1000 clientes ficticios en Guayaquil.
- `requirements.txt` – Librerías necesarias para Python/Streamlit.

---

## 🚀 Cómo usar

### Opción 1: **Streamlit App**
1. Sube el archivo `.py` y el `.geojson` a [Streamlit Cloud](https://share.streamlit.io/) o a tu propio servidor (Ubuntu recomendado).
<img width="945" alt="image" src="https://github.com/user-attachments/assets/32ee24c9-8ad2-4d38-b56f-dd8299fbfcef" />
2. Configura el token de KoBoToolbox en `secrets`.

<img width="803" alt="Captura de pantalla 2025-06-25 214505" src="https://github.com/user-attachments/assets/a2834651-0ee9-452e-8f41-adddaee56346" />


3. Accede y filtra clientes por ID o coordenadas, con validación visual y recomendaciones automáticas.
<img width="956" alt="image" src="https://github.com/user-attachments/assets/06a629f3-7ab2-4179-bbd4-cbd7cfb196a2" />
<img width="941" alt="image" src="https://github.com/user-attachments/assets/2be09964-6091-4ea3-95e8-fda74d48a86d" />

### Opción 2: **Notebook Colab/Jupyter**
1. Abre `visor_clientes_colab_final.ipynb` en Google Colab o JupyterLab.
2. Sube el archivo `clientes_1000_guayaquil.geojson`.
3. Coloca tu token KoBo en la celda correspondiente.
4. Ejecuta todo y visualiza el cruce, mapas y tabla de clientes en zona peligrosa.
<img width="763" alt="image" src="https://github.com/user-attachments/assets/0c9168c6-03d3-4641-ac8e-d6c6597b96b6" />

---
### 📱 Guía: Crear el formulario de zonas peligrosas en KoBoToolbox
1. Inicia sesión en KoBoToolbox

https://kf.kobotoolbox.org/

2. Crea un nuevo proyecto

    Haz clic en "Nuevo proyecto"

    Nómbralo, por ejemplo: Zonas peligrosas Guayaquil

3. Añade preguntas clave
Pregunta	Tipo	Descripción
Nombre de la zona	Texto corto	Nombre del sector o barrio
Tipo de riesgo	Selección	Alta, Media, Baja
Observaciones	Texto largo	Descripción libre
Zona geográfica	Polígono	Dibuja la zona en el mapa (tipo polígono)

    Para la pregunta geográfica, elige Polígono y permite al usuario dibujar sobre el mapa en el teléfono.

4. Publica y distribuye

    Haz clic en "Publicar"

    Comparte el formulario con tu equipo

    Los usuarios pueden llenar el formulario desde la web o KoBoCollect en Android.
![Imagen de WhatsApp 2025-06-25 a las 22 10 17_7ee18927](https://github.com/user-attachments/assets/2684949a-9932-4266-b769-1ebdc5cdb6e1)
![Imagen de WhatsApp 2025-06-25 a las 22 10 53_43fadbe7](https://github.com/user-attachments/assets/68dcf142-2a20-4e68-8472-f40ab36e2a19)


6. Accede a los datos

    Las zonas dibujadas estarán disponibles para análisis geoespacial vía API o descarga GeoJSON.
## 🖼️ Arquitectura

![e16fb6a7-5d80-4161-8940-3da906f61d58-1](https://github.com/user-attachments/assets/61e5408a-9615-49bc-814f-6539deac1764)


---

## 🛠️ Requisitos

- Python 3.8+
- geopandas, pandas, folium, streamlit, shapely, requests, matplotlib

---

## 🤖 Créditos

Desarrollado por Erick Adiran Córdova Pérez.  
Con IA, Streamlit, GeoPandas y KoBoToolbox.
