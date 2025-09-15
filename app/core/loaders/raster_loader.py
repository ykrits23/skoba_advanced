# core/loaders/raster_loader.py
import os
from qgis.core import QgsRasterLayer
from app.core.loader import BaseLoader, LoaderError

class RasterLoader(BaseLoader):
    """Лоадер для растрових файлів: .tif, .tiff, .vrt ..."""
    def load(self, path: str) -> QgsRasterLayer:
        name = os.path.basename(path)
        # Другий параметр — ім'я шару; третій (provider) для растрових часто не потрібен
        layer = QgsRasterLayer(path, name)
        if not layer.isValid():
            raise LoaderError(f"Raster load failed: {path}")
        return layer
