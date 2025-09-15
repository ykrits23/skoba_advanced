from qgis.gui import QgsMapCanvas

class MapCanvas(QgsMapCanvas):
    """Обгортка для QgsMapCanvas з базовими інструментами"""
    def __init__(self, parent=None):
        super().__init__(parent)

    def zoom_full(self):
        self.zoomToFullExtent()
