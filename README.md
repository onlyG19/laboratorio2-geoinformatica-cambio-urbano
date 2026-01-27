# Laboratorio 2: Monitoreo de Cambio Urbano en San Bernardo

Este proyecto implementa un flujo completo de teledetección para analizar la expansión urbana en San Bernardo, Chile, durante el periodo 2016-2026 utilizando imágenes de **Sentinel-2**.

## 🚀 Estructura del Proyecto

*   `notebooks/`: Flujo paso a paso (Descarga, Procesamiento, Detección de Cambios, Análisis Zonal).
*   `app/`: Dashboard interactivo en Streamlit.
*   `scripts/`: Funciones modulares para descarga y cálculo de índices espectrales.
*   `data/`: Almacenamiento de datos crudos (ZIP), procesados (TIF) y vectoriales (GPKG).

## 🛠️ Requisitos e Instalación

Asegúrate de tener Docker instalado para correr el entorno de desarrollo:

```bash
docker-compose up -d
```

## 📊 Ejecución de la Entrega Final

Para ver los resultados finales de forma interactiva y descargar las estadísticas:

1.  Asegúrate de haber ejecutado los Notebooks 02 y 04 completamente.
2.  Accede al dashboard en tu navegador:
    *   **URL:** [http://localhost:8501](http://localhost:8501)

## 📑 Entregables Incluidos (Parte 5)

*   **Aplicación Streamlit funcional**: Dashboard integrado con mapas y gráficos.
*   **Mapa Interactivo**: Capa coroplética de urbanización por cuadrantes de 500m.
*   **Gráficos Dinámicos**: Trayectorias temporales de NDVI, NDBI, etc.
*   **Comparador Visual**: Renderizado automático de rasters antes/después.
*   **Descarga**: Botón de descarga para las estadísticas en formato CSV.
