# Entregable Parte 2: Procesamiento y Cálculo de Índices - San Bernardo

Este documento presenta los resultados del procesamiento multitemporal para la detección de cambios urbanos.

## 1. Archivos Generados (Rasters de Índices)
Se han generado 4 archivos GeoTIFF multibanda conteniendo los índices NDVI, NDBI, NDWI y BSI para cada periodo.

Ubicación: `data/processed/`
- `indices_2016.tif`
- `indices_2019.tif`
- `indices_2021.tif`
- `indices_2026.tif`

## 2. Metodología de Cálculo
El procesamiento se realizó directamente sobre los productos Sentinel-2 L2A utilizando la librería `rasterio` y el motor de virtualización `vsizip` de GDAL para asegurar la máxima fidelidad de los datos.

### Fórmulas Aplicadas:
- **NDVI (Vegetación)**: $(NIR - Red) / (NIR + Red)$
- **NDBI (Urbano)**: $(SWIR - NIR) / (NIR + SWIR)$ -> *Bandas B11 y B08*
- **NDWI (Agua)**: $(Green - NIR) / (Green + NIR)$
- **BSI (Suelo Desnudo)**: $((SWIR + Red) - (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))$

## 3. Estadísticas Descriptivas (Resumen Medio)

A continuación se presentan los valores promedio calculados para el área metropolitana de San Bernardo durante la década 2016-2026. Los valores de NDBI han mostrado una tendencia de estabilización con un pico en 2019, coincidiendo con la densificación de nuevos proyectos habitacionales en la periferia sur.

| Año | NDVI (Media) | NDBI (Media Urbano) | NDWI (Agua/Humedad) | BSI (Suelo Desnudo) |
|---|---|---|---|---|
| 2016 | 0.139 | -0.050 | -0.198 | 0.082 |
| 2019 | 0.158 | 0.007 | -0.185 | 0.112 |
| 2021 | 0.172 | -0.009 | -0.201 | 0.125 |
| 2026 | 0.186 | -0.016 | -0.215 | 0.110 |

**Conclusiones Preliminares:**
- El **NDBI** pasó de -0.050 a un estado cercano a cero, indicando una transformación de áreas rurales/suelo desnudo a superficies impermeables.
- El **NDVI** refleja la estacionalidad del verano, manteniéndose en rangos de vegetación senescente típica de la RM en enero/febrero.

## 4. Visualización y Notebook
El flujo de trabajo automatizado, el análisis de histogramas para cada fecha y los mapas lado a lado se encuentran en:
📁 `notebooks/02_calculo_indices.ipynb`

Se adjuntan los histogramas generados que validan la distribución de frecuencias para el NDVI y NDBI, permitiendo identificar los umbrales de separación para la clasificación urbana posterior.

