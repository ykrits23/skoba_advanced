# ui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox,
    QVBoxLayout, QWidget, QAction, QProgressDialog
)
from qgis.gui import QgsMapCanvas
from app.core.qt_layer_manager import QtLayerManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SKOBA Pro")
        self.resize(900, 700)

        # Канвас карти
        self.canvas = QgsMapCanvas()

        # Статусний лейбл
        self.label = QLabel("No layer loaded")

        # Кнопка "Open"
        self.button = QPushButton("Open Data")
        self.button.clicked.connect(self.open_file_dialog)

        # Менеджер шарів
        self.layer_manager = QtLayerManager()
        self.layer_manager.layerAdded.connect(self.on_layer_added)
        self.layer_manager.loadStarted.connect(self.on_load_started)
        self.layer_manager.loadFinished.connect(self.on_load_finished)
        self.layer_manager.loadFailed.connect(self.on_load_failed)

        # Progress dialog (індикація завантаження)
        self.progress = None  # буде QProgressDialog при завантаженні

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Меню File → Open
        open_action = QAction("Open Data", self)
        open_action.triggered.connect(self.open_file_dialog)
        self.menuBar().addMenu("File").addAction(open_action)

    def open_file_dialog(self):
        filters = (
            "All supported (*.shp *.geojson *.gpkg *.tif *.tiff *.vrt);;"
            "Shapefiles (*.shp);;GeoPackage (*.gpkg);;GeoJSON (*.geojson *.json);;"
            "GeoTIFF (*.tif *.tiff)"
        )
        path, _ = QFileDialog.getOpenFileName(self, "Open data", "", filters)
        if not path:
            return
        # Викликаємо асинхронне завантаження
        self.layer_manager.load_async(path)

    # --- сигнали менеджера ---
    def on_load_started(self, path: str):
        # показуємо індикатор прогресу (без числа, просто busy)
        self.progress = QProgressDialog(f"Loading {path}...", None, 0, 0, self)
        self.progress.setWindowTitle("Loading")
        self.progress.setCancelButton(None)
        self.progress.setModal(True)
        self.progress.show()
        self.label.setText(f"Loading: {path}")

    def on_load_finished(self, layer):
        # прогрес приховуємо в on_layer_added (або тут)
        if self.progress:
            self.progress.hide()
            self.progress = None
        # label updated in on_layer_added
        # (але додатково можна тут зробити інші дії)
        # self.label.setText(f"Loaded: {layer.name()}")
        pass

    def on_load_failed(self, msg: str):
        if self.progress:
            self.progress.hide()
            self.progress = None
        QMessageBox.critical(self, "Load error", msg)
        self.label.setText("Load failed")

    def on_layer_added(self, layer):
        """Оновлюємо canvas з усіма шарами"""
        self.canvas.setLayers(self.layer_manager.get_layers())
        self.canvas.zoomToFullExtent()
        self.label.setText(f"Loaded: {layer.name()}")
