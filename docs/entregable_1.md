# Entregable Parte 1: Adquisición de Datos - San Bernardo (ACTUALIZADO)

Este documento cumple con los requisitos de la Parte 1 del Laboratorio de Detección de Cambios Urbanos.

## 1. Imágenes Seleccionadas
Se han seleccionado 4 imágenes del sensor **Sentinel-2 (MSI)**, formato **L2A (Reflectancia de Superficie)** en formato .SAFE.

| ID | Periodo | Sensor | Nubosidad (%) | Justificación |
|---|---|---|---|---|
| S2_2016 | Febrero 2016 | Sentinel-2A | < 1% | Imagen base histórica al inicio de la misión Sentinel-2. |
| S2_2019 | Verano 2019 | Sentinel-2A | < 1% | Referencia intermedia para análisis de tendencias pre-pandemia. |
| S2_2021 | Verano 2021 | Sentinel-2B | < 1% | Captura de expansión urbana durante el periodo 2019-2021. |
| S2_2026 | Enero 2026 | Sentinel-2 | < 1% | Estado actual para cierre de serie temporal (10 años de análisis). |

## 2. Metadatos de los Productos
Los productos descargados corresponden a la colección **COPERNICUS/S2_SR_HARMONIZED** (Nivel 2A), lo que garantiza:
- Corrección atmosférica de reflectancia de superficie (BOA).
- Resolución espacial de 10m para bandas visibles y NIR.
- Georreferenciación ortorectificada bajo el datum WGS84 / UTM zone 19S (EPSG:32719).

## 3. Justificación de Fechas
Las fechas fueron seleccionadas bajo los siguientes criterios técnico-geográficos:
- **Estacionalidad (Verano)**: En San Bernardo (Región Metropolitana), los meses de enero y febrero presentan la menor frecuencia de nubosidad y calima.
- **Detección Urbana**: El suelo seco de verano permite un contraste espectral superior entre el asfalto/concreto y las zonas agrícolas circundantes, fundamental para los índices NDBI y NDVI.

## 4. Script de Descarga Documentado
La búsqueda se realizó programáticamente para identificar los mejores productos (Least Cloud Cover) antes de la descarga manual desde Copernicus Browser.

```python
import pystac_client

# Configuración de búsqueda STAC para San Bernardo
BBOX = [-70.85, -33.67, -70.60, -33.50]
YEARS = [2016, 2019, 2021, 2026]

# Búsqueda de productos L2A con < 5% de nubes
# [Código documentado en scripts/download_sentinel.py]
```
