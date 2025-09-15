# core/loaders/vector_loader.py
import os
from qgis.core import QgsVectorLayer
from app.core.loader import BaseLoader, LoaderError

class VectorLoader(BaseLoader):
    """Лоадер для векторних файлів: .shp, .geojson, .gpkg, ..."""
    def load(self, path: str) -> QgsVectorLayer:
        name = os.path.basename(path)
        layer = QgsVectorLayer(path, name, "ogr")
        if not layer.isValid():
            raise LoaderError(f"Vector load failed: {path}")
        return layer
