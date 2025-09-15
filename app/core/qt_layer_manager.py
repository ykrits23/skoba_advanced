# app/core/qt_layer_manager.py
import os
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool
from qgis.core import QgsProject
from .loader import loader_registry, LoaderError   # Відносний імпорт

class _LoadWorkerSignals(QObject):
    finished = pyqtSignal(object)  # emits layer
    error = pyqtSignal(str)        # emits error message

class _LoadWorker(QRunnable):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.signals = _LoadWorkerSignals()

    def run(self):
        try:
            loader = loader_registry.get_loader_for(self.path)
            layer = loader.load(self.path)
            self.signals.finished.emit(layer)
        except Exception as e:
            self.signals.error.emit(str(e))

class QtLayerManager(QObject):
    layerAdded = pyqtSignal(object)
    loadStarted = pyqtSignal(str)
    loadFinished = pyqtSignal(object)
    loadFailed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layers = []
        self._pool = QThreadPool.globalInstance()

    def get_layers(self):
        return list(self._layers)

    def add_vector_layer(self, path: str):
        try:
            loader = loader_registry.get_loader_for(path)
            layer = loader.load(path)
            QgsProject.instance().addMapLayer(layer)
            self._layers.append(layer)
            self.layerAdded.emit(layer)
            self.loadFinished.emit(layer)
            return layer
        except Exception as e:
            self.loadFailed.emit(str(e))
            raise

    def load_async(self, path: str):
        self.loadStarted.emit(path)
        worker = _LoadWorker(path)
        worker.signals.finished.connect(self._on_worker_finished)
        worker.signals.error.connect(self._on_worker_error)
        self._pool.start(worker)

    def _on_worker_finished(self, layer):
        QgsProject.instance().addMapLayer(layer)
        self._layers.append(layer)
        self.layerAdded.emit(layer)
        self.loadFinished.emit(layer)

    def _on_worker_error(self, msg: str):
        self.loadFailed.emit(msg)
