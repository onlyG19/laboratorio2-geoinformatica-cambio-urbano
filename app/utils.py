import rasterio
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
import streamlit as st
from config import DATA_PROCESSED, ZONES_FILE, LIMIT_FILE, STAT_FILE

@st.cache_data
def cargar_capas():
    if ZONES_FILE.exists():
        gdf = gpd.read_file(ZONES_FILE)
        # Limpiar nombres de columnas (quitar espacios, etc)
        gdf.columns = [c.strip() for c in gdf.columns]
        return gdf
    return None

@st.cache_data
def cargar_limite():
    if LIMIT_FILE.exists():
        return gpd.read_file(LIMIT_FILE)
    return None

@st.cache_data
def cargar_stats_temporales():
    if STAT_FILE.exists():
        return pd.read_csv(STAT_FILE)
    return None

def get_raster_img(año, mode, limite):
    f_path = DATA_PROCESSED / f"indices_{año}.tif"
    if f_path.exists():
        with rasterio.open(f_path) as src:
            idx = 1 if mode == "NDVI" else 2
            data = src.read(idx)
            
            limite_utm = limite.to_crs(src.crs)
            minx, miny, maxx, maxy = limite_utm.total_bounds
            marx = (maxx - minx) * 0.15
            mary = (maxy - miny) * 0.15
            
            fig, ax = plt.subplots(figsize=(10, 8))
            cmap = 'viridis' if mode == "NDVI" else 'magma'
            vmin, vmax = (-0.2, 0.8) if mode == "NDVI" else (-0.1, 0.4)
            
            extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
            ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, extent=extent)
            limite_utm.plot(ax=ax, edgecolor='cyan', facecolor='none', linestyle='--', linewidth=2)
            
            ax.set_xlim(minx - marx, maxx + marx)
            ax.set_ylim(miny - mary, maxy + mary)
            ax.axis('off')
            return fig
    return None
