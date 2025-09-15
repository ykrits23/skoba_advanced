
import sys, os

QGIS_PREFIX = r"C:\Program Files\QGIS 3.34.8\apps\qgis-ltr"
QGIS_BIN = r"C:\Program Files\QGIS 3.34.8\bin"
QGIS_PYTHON = os.path.join(QGIS_PREFIX, "python")
QGIS_PYTHON_SITEPACKAGES = r"C:\Program Files\QGIS 3.34.8\apps\Python39\Lib\site-packages"

# 1) DLL-ша шлях (потрібно щоб _core.pyd міг знайти залежності)
os.environ['PATH'] = QGIS_BIN + os.pathsep + os.environ.get('PATH', '')

# 2) QGIS PREFIX
os.environ['QGIS_PREFIX_PATH'] = QGIS_PREFIX

# 3) python шляхи (спочатку qgis python, потім site-packages з PyQt5)
for p in (QGIS_PYTHON, QGIS_PYTHON_SITEPACKAGES):
    if p and p not in sys.path:
        sys.path.insert(0, p)

# ----------------------------
# Тільки тепер імпортуємо QGIS
# ----------------------------
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel

# Ініціалізація QGIS
qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX, True)
qgs.initQgis()

# ----------------------------
# GUI
# ----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGIS SHP Viewer")
        self.setGeometry(200, 200, 800, 600)

        self.canvas = QgsMapCanvas(self)
        self.canvas.setGeometry(10, 50, 780, 540)

        self.label = QLabel("No layer loaded", self)
        self.label.setGeometry(10, 10, 300, 30)

        self.button = QPushButton("Open SHP", self)
        self.button.setGeometry(350, 10, 100, 30)
        self.button.clicked.connect(self.open_shp)

    def open_shp(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Shapefile", "", "*.shp")
        if path:
            layer = QgsVectorLayer(path, os.path.basename(path), "ogr")
            if not layer.isValid():
                self.label.setText("Failed to load layer")
                return
            QgsProject.instance().addMapLayer(layer)
            self.canvas.setLayers([layer])
            self.canvas.zoomToFullExtent()
            self.label.setText(f"Loaded: {os.path.basename(path)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    result = app.exec_()
    qgs.exitQgis()
    sys.exit(result)

if __name__ == "__main__":
    main()
