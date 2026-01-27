import rasterio
from rasterio.enums import Resampling
import numpy as np
from pathlib import Path
import zipfile
import re
import os

def get_band_path_in_zip(zip_obj, band_suffix, resolution='10m'):
    """Busca el path de una banda específica dentro del ZIP de Sentinel-2 L2A."""
    pattern = re.compile(f".*_{band_suffix}_{resolution}\\.jp2$")
    for name in zip_obj.namelist():
        if pattern.match(name):
            return name
    # Si no la encuentra en 10m (como la B11), busca en 20m
    if resolution == '10m':
        return get_band_path_in_zip(zip_obj, band_suffix, resolution='20m')
    return None

def calcular_indices_from_zip(ruta_zip, ruta_salida):
    print(f"📦 Procesando ZIP: {ruta_zip.name}...")
    
    with zipfile.ZipFile(ruta_zip, 'r') as z:
        # Encontrar paths internos
        b_paths = {
            'blue': get_band_path_in_zip(z, 'B02'),
            'green': get_band_path_in_zip(z, 'B03'),
            'red': get_band_path_in_zip(z, 'B04'),
            'nir': get_band_path_in_zip(z, 'B08'),
            'swir': get_band_path_in_zip(z, 'B11', '20m') # B11 es nativa 20m
        }

        # Leer bandas usando /vsizip/ de GDAL
        data = {}
        with rasterio.Env(GDAL_NUM_THREADS='ALL_CPUS'):
            # Leer banda de referencia (Rojo) para obtener dimensiones 10m
            ref_path = f"/vsizip/{ruta_zip}/{b_paths['red']}"
            with rasterio.open(ref_path) as ref:
                out_shape = (ref.height, ref.width)
                profile = ref.profile
                transform = ref.transform

            for band, internal_path in b_paths.items():
                vsi_path = f"/vsizip/{ruta_zip}/{internal_path}"
                with rasterio.open(vsi_path) as src:
                    # Resampling a 10m si es necesario (especialmente para SWIR)
                    data[band] = src.read(
                        1, 
                        out_shape=out_shape, 
                        resampling=Resampling.bilinear
                    ).astype(float) / 10000.0

        # Cálculo de Índices
        eps = 1e-10
        ndvi = (data['nir'] - data['red']) / (data['nir'] + data['red'] + eps)
        ndbi = (data['swir'] - data['nir']) / (data['swir'] + data['nir'] + eps)
        ndwi = (data['green'] - data['nir']) / (data['green'] + data['nir'] + eps)
        bsi = ((data['swir'] + data['red']) - (data['nir'] + data['blue'])) / \
              ((data['swir'] + data['red']) + (data['nir'] + data['blue']) + eps)

        # Guardar
        profile.update(count=4, dtype='float32', driver='GTiff', nodata=np.nan)
        with rasterio.open(ruta_salida, 'w', **profile) as dst:
            dst.write(ndvi.astype('float32'), 1)
            dst.write(ndbi.astype('float32'), 2)
            dst.write(ndwi.astype('float32'), 3)
            dst.write(bsi.astype('float32'), 4)
            dst.set_band_description(1, 'NDVI')
            dst.set_band_description(2, 'NDBI')
            dst.set_band_description(3, 'NDWI')
            dst.set_band_description(4, 'BSI')
            
    return {'ndvi': ndvi, 'ndbi': ndbi}

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    raw_path = project_root / 'data' / 'raw'
    proc_path = project_root / 'data' / 'processed'
    
    zips = list(raw_path.glob('*.zip'))
    for z in zips:
        # Busca 4 dígitos seguidos (el año) en el nombre del archivo
        match = re.search(r'(\d{4})', z.name)
        if match:
            year = match.group(1)
            salida = proc_path / f"indices_{year}.tif"
            try:
                res = calcular_indices_from_zip(z, salida)
                print(f"✅ Éxito {year}: NDBI medio = {np.nanmean(res['ndbi']):.3f}")
            except Exception as e:
                print(f"❌ Error en {z.name}: {e}")
        else:
            print(f"⚠️ No se pudo extraer el año de: {z.name}")
