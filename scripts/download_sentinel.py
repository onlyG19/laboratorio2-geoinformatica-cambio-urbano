import pystac_client
import odc.stac
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN ---
# Coordenadas San Bernardo, Chile [Longitud min, Latitud min, Longitud max, Latitud max]
BBOX = [-70.85, -33.67, -70.60, -33.50]
YEARS = [2016, 2018, 2020, 2022, 2024, 2026]
CLOUD_LIMIT = 5
COLLECTION = "sentinel-2-l2a"
# ---------------------

def run_stac_search():
    print(f"Buscando imágenes en Sentinel-2 L2A para San Bernardo...")
    catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
    
    for year in YEARS:
        date_range = f"{year}-01-01/{year}-03-31"
        search = catalog.search(
            collections=[COLLECTION],
            bbox=BBOX,
            datetime=date_range,
            query={"eo:cloud_cover": {"lt": CLOUD_LIMIT}},
            sortby=[{"field": "properties.eo:cloud_cover", "direction": "asc"}]
        )
        
        items = list(search.items())
        if items:
            best_item = items[0]
            print(f"[{year}] Encontrada: {best_item.id} | Nubes: {best_item.properties['eo:cloud_cover']}%")
            # Aquí podrías agregar lógica para descargar bandas específicas si fuera necesario
        else:
            print(f"[{year}] No se encontraron imágenes con menos de {CLOUD_LIMIT}% de nubes.")

if __name__ == "__main__":
    run_stac_search()
    print("\nProcedimiento de script documentado finalizado.")
    print("Nota: Para descarga masiva manual, use las fechas anteriores en Copernicus Browser.")
