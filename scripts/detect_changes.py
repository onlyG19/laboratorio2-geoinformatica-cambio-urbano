import numpy as np
import rasterio

def detectar_cambio_diferencia(ruta_t1, ruta_t2, umbral=0.15):
    """
    Detecta cambios usando diferencia de NDVI.
    
    Returns:
        cambio: array con valores -1 (perdida), 0 (sin cambio), 1 (ganancia)
        diferencia: array con los valores netos
        profile: perfil del raster
    """
    with rasterio.open(ruta_t1) as src1:
        ndvi_t1 = src1.read(1)
        profile = src1.profile
    
    with rasterio.open(ruta_t2) as src2:
        ndvi_t2 = src2.read(1)
    
    diferencia = ndvi_t2 - ndvi_t1
    cambio = np.zeros_like(diferencia, dtype=np.int8)
    cambio[diferencia < -umbral] = -1
    cambio[diferencia > umbral] = 1
    
    return cambio, diferencia, profile

def clasificar_cambio_urbano(indices_t1, indices_t2, umbrales=None):
    """
    Clasifica el tipo de cambio urbano usando multiples indices.
    
    Clases:
        0: Sin cambio
        1: Urbanizacion
        2: Perdida vegetacion
        3: Ganancia vegetacion
    """
    if umbrales is None:
        umbrales = {
            'ndvi_veg': 0.3,
            'ndbi_urbano': 0.0,
            'cambio_min': 0.1
        }
    
    clase = np.zeros_like(indices_t1[0], dtype=np.uint8)
    
    # Urbanizacion
    es_urbanizacion = (indices_t1[1] < 0) & (indices_t2[1] > 0)
    # Perdida vegetacion
    perdio_veg = (indices_t1[0] - indices_t2[0]) > umbrales['cambio_min']
    
    clase[es_urbanizacion] = 1
    clase[perdio_veg & (clase == 0)] = 2
    clase[(indices_t2[0] - indices_t1[0]) > umbrales['cambio_min']] = 3
    
    return clase
