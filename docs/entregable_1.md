# Entregable Parte 1: Adquisición de Datos - San Bernardo (ACTUALIZADO)

Este documento cumple con los requisitos de la Parte 1 del Laboratorio de Detección de Cambios Urbanos.

## 1. Imágenes Seleccionadas
Se han seleccionado 6 imágenes del sensor **Sentinel-2 (MSI)**, formato **L2A (Reflectancia de Superficie)** en formato .SAFE.

| ID | Periodo | Sensor | Nubosidad (%) | Justificación |
|---|---|---|---|---|
| BASE_2016 | Marzo 2016 | Sentinel-2A | < 1% | Imagen base histórica al inicio de la misión Sentinel-2. |
| INTER_2017 | Noviembre 2017 | Sentinel-2B | < 1% | Captura del pico de vigor vegetal (Primavera). |
| INTER_2019 | Mayo 2019 | Sentinel-2B | < 1% | Primer cruce positivo de NDBI: Inicio de expansión detectada. |
| INTER_2021 | Marzo 2021 | Sentinel-2B | < 1% | Estabilización y consolidación de proyectos pre-existentes. |
| REC_2023 | Octubre 2023 | Sentinel-2A | < 1% | Variación por humedad/suelo desnudo activo (Primavera). |
| FINAL_2026 | Enero 2026 | Sentinel-2C | < 1% | Estado final: Densidad urbana consolidada (10 años). |

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
YEARS = [2016, 2017, 2019, 2021, 2023, 2026]

# Búsqueda de productos L2A con < 5% de nubes
# [Código documentado en scripts/download_sentinel.py]
```
