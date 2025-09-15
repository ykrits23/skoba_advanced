import os
from qgis.core import QgsVectorLayer, QgsProject

def load_vector_layer(path: str, provider: str = "ogr") -> QgsVectorLayer:
    """
    Завантажити векторний шар, додати у QgsProject і повернути його.
    Кидає IOError якщо шар не валідний.
    """
    if not path:
        raise ValueError("Empty path")

    name = os.path.basename(path)
    layer = QgsVectorLayer(path, name, provider)

    if not layer.isValid():
        raise IOError(f"Failed to load layer: {path}")

    QgsProject.instance().addMapLayer(layer)
    return layer
