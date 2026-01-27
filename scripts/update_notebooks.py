import nbformat as nbf
from pathlib import Path

def update_notebook_01():
    path = Path('/home/byron/Escritorio/projectos/laboratorio2-cambio-urbano/notebooks/01_descarga_datos.ipynb')
    if not path.exists(): return
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Cell 1: Markdown intro
    nb.cells[0].source = "# Laboratorio 2: 01 Descarga y Preprocesamiento\n\nEste notebook implementa la **Parte 1** del laboratorio: la descarga de imágenes Sentinel-2 y el recorte al área de estudio (San Bernardo) para un análisis multitemporal (2016-2026)."

    # Cell 2: Markdown context
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and 'Se han seleccionado 4 periodos temporales' in cell.source:
            cell.source = "## 1. Contexto de Adquisición\n\nSe han seleccionado 6 periodos temporales para analizar la expansión urbana de San Bernardo:\n- **2016**: Inicio de la serie temporal.\n- **2018**: Seguimiento bienal.\n- **2020**: Seguimiento bienal.\n- **2022**: Seguimiento bienal.\n- **2024**: Seguimiento bienal.\n- **2026**: Estado actual.\n\n**Método de descarga:** Copernicus Data Space Browser (Manual) y búsqueda vía STAC API (Programática)."
            break

    # Cell 3: Code (stac_search)
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'years = [2016, 2019, 2021, 2026]' in cell.source:
            cell.source = cell.source.replace('years = [2016, 2019, 2021, 2026]', 'years = [2016, 2018, 2020, 2022, 2024, 2026]')
            break

    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

def update_notebook_02():
    path = Path('/home/byron/Escritorio/projectos/laboratorio2-cambio-urbano/notebooks/02_calculo_indices.ipynb')
    if not path.exists(): return
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Cell 1: Markdown
    nb.cells[0].source = "# Laboratorio 2: 02 Cálculo de Índices Espectrales\n\nEste notebook implementa la **Parte 2** del laboratorio, enfocándose en el cálculo de NDVI y NDBI para las imágenes Sentinel-2 procesadas del periodo 2016-2026."

    # Cell 2: Code (config)
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'years = [2019, 2021, 2023, 2026]' in cell.source:
            cell.source = cell.source.replace('years = [2019, 2021, 2023, 2026]', 'years = [2016, 2018, 2020, 2022, 2024, 2026]')
            break

    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

def update_notebook_03():
    path = Path('/home/byron/Escritorio/projectos/laboratorio2-cambio-urbano/notebooks/03_deteccion_cambios.ipynb')
    if not path.exists(): return
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Cell 1: Markdown
    nb.cells[0].source = "# Laboratorio 2: 03 Detección de Cambios Urbanos\n\nEste notebook implementa la **Parte 3** del laboratorio, enfocándose en la detección de cambios multitemporales entre 2016 y 2026 en la comuna de San Bernardo.\n\n---"

    # Cell 2: Code (config)
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'indices_2019.tif' in cell.source:
            cell.source = cell.source.replace('indices_2019.tif', 'indices_2016.tif')
            break

    # Cell 4: Plot title
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'M1: Diferencia NDVI (2019-2026)' in cell.source:
            cell.source = cell.source.replace('M1: Diferencia NDVI (2019-2026)', 'M1: Diferencia NDVI (2016-2026)')
            break

    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

def update_notebook_04():
    path = Path('/home/byron/Escritorio/projectos/laboratorio2-cambio-urbano/notebooks/04_analisis_zonal.ipynb')
    if not path.exists(): return
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Cell 1: Markdown
    nb.cells[0].source = "# Laboratorio 2: 04 Cuantificación y Análisis Zonal\n\nEste notebook implementa la **Parte 4**, enfocándose en la cuantificación de áreas de cambio y el análisis temporal de los índices espectrales (2016-2026)."

    # Cell 3: Print
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'Total Urbanización Detectada (2016-2026)' in cell.source:
            cell.source = cell.source.replace('2019-2026', '2016-2026')
            break
    
    # Cell 5: Plot title
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'Tendencias Espectrales Promedio (2016-2026)' in cell.source:
            cell.source = cell.source.replace('2019-2026', '2016-2026')
            break

    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    update_notebook_01()
    update_notebook_02()
    update_notebook_03()
    update_notebook_04()
    print("Notebooks corrected and updated successfully.")
