import rasterio
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import re
import imageio.v2 as imageio
import os
import geopandas as gpd

def generar_gif(proc_path, vector_path, fig_path, modo, nombre_archivo, cmap, vmin, vmax, titulo_prefijo, limite):
    indices_files = sorted(proc_path.glob('indices_*.tif'))
    frames = []
    print(f"🎬 Generando frames para {modo}...")
    for f in indices_files:
        year = re.search(r'\d{4}', f.name).group()
        with rasterio.open(f) as src:
            idx = 1 if modo == 'NDVI' else 2
            data = src.read(idx)
            
            limite_utm = limite.to_crs(src.crs)
            minx, miny, maxx, maxy = limite_utm.total_bounds
            margin = (maxx - minx) * 0.15
            
            fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
            extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
            ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, extent=extent)
            limite_utm.plot(ax=ax, edgecolor='cyan', facecolor='none', linestyle='--', linewidth=3)
            
            ax.set_xlim(minx - margin, maxx + margin)
            ax.set_ylim(miny - margin, maxy + margin)
            ax.set_title(f"{titulo_prefijo}: {year}", fontsize=25, color='white', pad=20)
            ax.axis('off')
            
            fig.patch.set_facecolor('#0e1117')
            plt.tight_layout()
            
            temp_png = f"temp_{modo}_{year}.png"
            plt.savefig(temp_png, facecolor=fig.get_facecolor())
            plt.close()
            
            frames.append(imageio.imread(temp_png))
            os.remove(temp_png)

    imageio.mimsave(fig_path / nombre_archivo, frames, duration=1000, loop=0)
    print(f"✅ GIF {nombre_archivo} generado con éxito!")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    proc_path = project_root / 'data' / 'processed'
    vector_path = project_root / 'data' / 'vector'
    fig_path = project_root / 'outputs' / 'figures'
    fig_path.mkdir(exist_ok=True, parents=True)
    
    limite = gpd.read_file(vector_path / 'limite_comuna.gpkg')
    
    generar_gif(proc_path, vector_path, fig_path, 'NDBI', 'evolucion_urbana.gif', 'magma', -0.1, 0.4, 'Expansión Urbana', limite)
    generar_gif(proc_path, vector_path, fig_path, 'NDVI', 'evolucion_vegetacion.gif', 'viridis', -0.2, 0.8, 'Vigor Vegetación', limite)
