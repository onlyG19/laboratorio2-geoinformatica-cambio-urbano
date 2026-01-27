import rasterio
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
import re
from detect_changes import clasificar_cambio_urbano
from zonal_analysis import analisis_zonal_cambios

def update_temporal_stats(proc_path):
    print("📈 Actualizando estadísticas temporales...")
    files = sorted(list(proc_path.glob("indices_*.tif")))
    rows = []
    
    for f in files:
        year = re.search(r'(\d{4})', f.name).group()
        with rasterio.open(f) as src:
            # 1: NDVI, 2: NDBI, 3: NDWI, 4: BSI
            ndvi = src.read(1)
            ndbi = src.read(2)
            ndwi = src.read(3)
            bsi = src.read(4)
            
            rows.append({
                "Año": int(year),
                "NDVI_media": np.nanmean(ndvi),
                "NDVI_std": np.nanstd(ndvi),
                "NDBI_media": np.nanmean(ndbi),
                "NDBI_std": np.nanstd(ndbi),
                "NDWI_media": np.nanmean(ndwi),
                "NDWI_std": np.nanstd(ndwi),
                "BSI_media": np.nanmean(bsi),
                "BSI_std": np.nanstd(bsi)
            })
    
    df = pd.DataFrame(rows).sort_values("Año")
    df.to_csv(proc_path / "estadisticas_cambio.csv", index=False)
    print(f"✅ CSV guardado con {len(df)} fechas.")
    return df

def update_zonal_map(proc_path, vector_path):
    print("🗺️ Actualizando mapa zonal (2016 - 2026)...")
    
    f16 = proc_path / "indices_2016.tif"
    f26 = proc_path / "indices_2026.tif"
    
    if not (f16.exists() and f26.exists()):
        print("❌ Faltan archivos 2016 o 2026.")
        return
    
    with rasterio.open(f16) as src16, rasterio.open(f26) as src26:
        indices_t1 = (src16.read(1), src16.read(2)) # NDVI, NDBI
        indices_t2 = (src26.read(1), src26.read(2))
        profile = src16.profile
        
        cambio = clasificar_cambio_urbano(indices_t1, indices_t2)
        
        cambio_path = proc_path / "cambio_clasificado.tif"
        profile.update(count=1, dtype='uint8', nodata=0)
        with rasterio.open(cambio_path, 'w', **profile) as dst:
            dst.write(cambio, 1)
    
    # Análisis Zonal
    limite = gpd.read_file(vector_path / "limite_comuna.gpkg")
    # Generar grilla de 500m (como en zonal_analysis.py)
    from zonal_analysis import crear_grilla
    zones_gdf = crear_grilla(limite, size=500)
    
    resultado = analisis_zonal_cambios(cambio_path, zones_gdf)
    resultado.to_file(vector_path / "zonas_cambio.gpkg", driver="GPKG")
    print("✅ zonas_cambio.gpkg actualizado.")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    proc_path = project_root / 'data' / 'processed'
    vector_path = project_root / 'data' / 'vector'
    
    update_temporal_stats(proc_path)
    update_zonal_map(proc_path, vector_path)
