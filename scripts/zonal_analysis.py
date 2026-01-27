import geopandas as gpd
import pandas as pd
import numpy as np
from rasterstats import zonal_stats
from shapely.geometry import box

def crear_grilla(gdf, size=500):
    """Crea una grilla regular sobre el area de estudio."""
    xmin, ymin, xmax, ymax = gdf.total_bounds
    cols = list(np.arange(xmin, xmax + size, size))
    rows = list(np.arange(ymin, ymax + size, size))
    
    polygons = []
    for x in cols[:-1]:
        for y in rows[:-1]:
            polygons.append(box(x, y, x + size, y + size))
    
    grid = gpd.GeoDataFrame({'geometry': polygons}, crs=gdf.crs)
    grid = gpd.overlay(grid, gdf, how='intersection')
    grid['ID_ZONA'] = range(len(grid))
    return grid

def analisis_zonal_cambios(ruta_cambios, zones_gdf):
    """Calcula estadisticas de cambio por zona."""
    stats = zonal_stats(
        zones_gdf, ruta_cambios,
        categorical=True,
        category_map={0: 'sin_cambio', 1: 'urbanizacion', 2: 'perdida_veg', 3: 'ganancia_veg'}
    )
    df_stats = pd.DataFrame(stats).fillna(0)
    resultado = pd.concat([zones_gdf.reset_index(drop=True), df_stats], axis=1)
    
    # 1 pixel Sentinel-2 = 100m2 = 0.01 Ha
    resultado['urb_ha'] = resultado.get('urbanizacion', 0) * 0.01
    return resultado
