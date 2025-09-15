# app/core/__init__.py
from .loader import loader_registry
from .loaders.vector_loader import VectorLoader
from .loaders.raster_loader import RasterLoader

def register_default_loaders():
    """
    Зареєструвати стандартні лоадери (викликається явно з main.py).
    idempotent — можна викликати декілька разів.
    """
    mapping = {
        ".shp": VectorLoader(),
        ".geojson": VectorLoader(),
        ".gpkg": VectorLoader(),
        ".json": VectorLoader(),
        ".tif": RasterLoader(),
        ".tiff": RasterLoader(),
        ".vrt": RasterLoader(),
    }

    # перевірка існування, щоб не перезаписувати якщо вже є
    for ext, loader in mapping.items():
        if ext not in getattr(loader_registry, "_by_ext", {}):
            loader_registry.register(ext, loader)
