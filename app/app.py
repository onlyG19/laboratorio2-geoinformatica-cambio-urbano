import streamlit as st
import folium
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
import plotly.express as px
import re
from pathlib import Path

# Importes locales
from config import DATA_PROCESSED, COLOR_MAP_URB
from utils import cargar_capas, cargar_limite, cargar_stats_temporales, get_raster_img

# Configuración de página
st.set_page_config(page_title="Dashboard Cambio Urbano - San Bernardo", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #464855; }
    div[data-testid="stMetricValue"] { color: #ff4b4b !important; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Monitoreo de Cambio Urbano: San Bernardo (2016-2026)")
st.markdown("Analítica geoespacial avanzada basada en imágenes multiespectrales de Sentinel-2.")

# --- SIDEBAR ---
st.sidebar.header("🛠️ Configuración")

zonas = cargar_capas()
df_temporal = cargar_stats_temporales()
limite = cargar_limite()

path_indices = list(DATA_PROCESSED.glob("indices_*.tif"))
años_disponibles = sorted([int(re.search(r'\d{4}', f.name).group()) for f in path_indices]) if path_indices else [2016, 2019, 2021, 2026]

fecha_inicio = st.sidebar.selectbox("Fecha Inicial", años_disponibles, index=0)
fecha_fin = st.sidebar.selectbox("Fecha Final", años_disponibles, index=len(años_disponibles)-1)

if zonas is not None and limite is not None:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🗺️ Mapa de Intensidad de Urbanización")
        zonas_wgs84 = zonas.to_crs(epsg=4326)
        limite_wgs84 = limite.to_crs(epsg=4326)
        
        m = folium.Map(tiles="cartodbpositron")
        # Ajustar zoom a la comuna
        sw = limite_wgs84.bounds.iloc[0][['miny', 'minx']].tolist()
        ne = limite_wgs84.bounds.iloc[0][['maxy', 'maxx']].tolist()
        m.fit_bounds([sw, ne])
        
        # Verificar columnas antes de graficar
        if 'ID_ZONA' in zonas_wgs84.columns and 'urb_ha' in zonas_wgs84.columns:
            folium.Choropleth(
                geo_data=zonas_wgs84,
                name="Urbanización (Ha)",
                data=pd.DataFrame(zonas_wgs84.drop(columns='geometry')),
                columns=["ID_ZONA", "urb_ha"],
                key_on="feature.properties.ID_ZONA",
                fill_color=COLOR_MAP_URB,
                fill_opacity=0.6,
                line_opacity=0.1,
            ).add_to(m)
        else:
            st.error(f"Faltan columnas en los datos zonales. Columnas encontradas: {list(zonas_wgs84.columns)}")
        
        folium.GeoJson(
            limite_wgs84,
            name="Límite San Bernardo",
            style_function=lambda x: {'fillColor': 'none', 'color': '#00ffff', 'weight': 3, 'dashArray': '5, 5'}
        ).add_to(m)

        # Tooltips interactivos
        folium.GeoJson(
            zonas_wgs84,
            style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent'},
            tooltip=folium.GeoJsonTooltip(
                fields=['ID_ZONA', 'urb_ha'],
                aliases=['ID Zona:', 'Hectáreas (Ha):'],
                localize=True
            )
        ).add_to(m)
        
        st_folium(m, width=900, height=500, returned_objects=[])

    with col2:
        st.subheader("📊 Métricas de Cambio")
        total_ha = zonas['urb_ha'].sum()
        st.metric("Total Edificado (Ha)", f"{total_ha:.2f}")
        
        top_zonas = zonas.nlargest(12, 'urb_ha').sort_values('urb_ha', ascending=True)
        fig_top = px.bar(top_zonas, y=top_zonas['ID_ZONA'].astype(str), x='urb_ha', orientation='h',
                         title="Sectores de mayor expansión", color='urb_ha', color_continuous_scale='Reds')
        fig_top.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---")
    st.subheader("🌗 Comparativa Visual")
    idx_choice = st.radio("Capa Visual:", ["NDVI (Vegetación)", "NDBI (Urbano)"], horizontal=True)
    mode = "NDVI" if "NDVI" in idx_choice else "NDBI"
    
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"**🗓️ {fecha_inicio}**")
        fig_i = get_raster_img(fecha_inicio, mode, limite)
        if fig_i: st.pyplot(fig_i)
    with c4:
        st.markdown(f"**🗓️ {fecha_fin}**")
        fig_f = get_raster_img(fecha_fin, mode, limite)
        if fig_f: st.pyplot(fig_f)

    if df_temporal is not None:
        st.markdown("---")
        st.subheader("📈 Evolución Temporal del Paisaje")
        
        # Gráfico de líneas arriba
        df_melt = df_temporal.melt(id_vars=["Año"], value_vars=["NDVI_media", "NDBI_media"], var_name="Índice")
        st.plotly_chart(px.line(df_melt, x="Año", y="value", color="Índice", markers=True), use_container_width=True)
        
        # Animaciones abajo en 2 columnas
        st.markdown("### 🎞️ Time-lapses de Cambio Geográfico")
        cg1, cg2 = st.columns(2)
        
        figs_dir = Path(__file__).resolve().parent.parent / "outputs" / "figures"
        
        with cg1:
            st.markdown("**🏙️ Expansión Urbana (NDBI)**")
            gif_urb = figs_dir / "evolucion_urbana.gif"
            if gif_urb.exists():
                st.image(str(gif_urb), use_container_width=True)
            else:
                st.info("Animación urbana no encontrada.")
                
        with cg2:
            st.markdown("**🌿 Vigor de Vegetación (NDVI)**")
            gif_veg = figs_dir / "evolucion_vegetacion.gif"
            if gif_veg.exists():
                st.image(str(gif_veg), use_container_width=True)
            else:
                st.info("Animación de vegetación no encontrada.")

    csv = zonas.drop(columns='geometry').to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Descargar CSV", csv, "stats.csv", "text/csv")
else:
    st.error("Faltan datos procesados.")
