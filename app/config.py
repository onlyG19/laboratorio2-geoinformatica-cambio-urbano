from pathlib import Path

# Raiz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de datos
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DATA_VECTOR = BASE_DIR / "data" / "vector"
OUTPUTS = BASE_DIR / "outputs"

# Archivos especificos
STAT_FILE = DATA_PROCESSED / "estadisticas_cambio.csv"
ZONES_FILE = DATA_VECTOR / "zonas_cambio.gpkg"
LIMIT_FILE = DATA_VECTOR / "limite_comuna.gpkg"

# Colores y Estilos
COLOR_MAP_URB = "YlOrRd"
COLORS_CLASES = ['#f0f0f0', '#e31a1c', '#ff7f00', '#33a02c', '#1f78b4']
