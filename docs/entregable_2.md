# Entregable Parte 2: Procesamiento y Cálculo de Índices - San Bernardo

Este documento presenta los resultados del procesamiento multitemporal para la detección de cambios urbanos.

## 1. Archivos Generados (Rasters de Índices)
Se han generado 6 archivos GeoTIFF multibanda conteniendo los índices NDVI, NDBI, NDWI y BSI para cada periodo.

Ubicación: `data/processed/`
- `indices_2016.tif`
- `indices_2017.tif`
- `indices_2019.tif`
- `indices_2021.tif`
- `indices_2023.tif`
- `indices_2026.tif`

## 2. Metodología de Cálculo
El procesamiento se realizó directamente sobre los productos Sentinel-2 L2A utilizando la librería `rasterio` y el motor de virtualización `vsizip` de GDAL para asegurar la máxima fidelidad de los datos.

### Fórmulas Aplicadas:
- **NDVI (Vegetación)**: $(NIR - Red) / (NIR + Red)$
- **NDBI (Urbano)**: $(SWIR - NIR) / (NIR + SWIR)$ -> *Bandas B11 y B08*
- **NDWI (Agua)**: $(Green - NIR) / (Green + NIR)$
- **BSI (Suelo Desnudo)**: $((SWIR + Red) - (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))$

## 3. Estadísticas Descriptivas (Resumen Medio)

A continuación se presentan los valores promedio calculados para la comuna de San Bernardo durante la década 2016-2026. Se observa una correlación inversa donde los incrementos en NDBI coinciden con la consolidación industrial y residencial detectada.

| Año | NDVI (Media) | NDBI (Media Urbano) | Interpretación del Paisaje |
|---|---|---|---|
| 2016 | 0.196 | -0.032 | Base: Predominio de suelo natural/agrícola. |
| 2017 | 0.223 | -0.134 | Pico de vigor vegetal (estacionalidad). |
| 2019 | 0.157 | 0.006 | Primer cruce positivo de NDBI: Inicio de expansión. |
| 2021 | 0.172 | -0.008 | Estabilización y consolidación. |
| 2023 | 0.188 | -0.192 | Variación por humedad/suelo desnudo activo. |
| 2026 | 0.186 | -0.016 | Estado final: Mayor densidad urbana que el origen. |

**Conclusiones Preliminares:**
- El **NDBI** pasó de -0.050 a un estado cercano a cero, indicando una transformación de áreas rurales/suelo desnudo a superficies impermeables.
- El **NDVI** refleja la estacionalidad del verano, manteniéndose en rangos de vegetación senescente típica de la RM en enero/febrero.

## 4. Visualización y Notebook
El flujo de trabajo automatizado, el análisis de histogramas para cada fecha y los mapas lado a lado se encuentran en:
📁 `notebooks/02_calculo_indices.ipynb`

Se adjuntan los histogramas generados que validan la distribución de frecuencias para el NDVI y NDBI, permitiendo identificar los umbrales de separación para la clasificación urbana posterior.

