# core/loader.py
import os
from typing import Dict
from qgis.core import QgsMapLayer

class LoaderError(RuntimeError):
    pass

class BaseLoader:
    """Інтерфейс лоадера: реалізуй load(path) -> QgsMapLayer"""
    def load(self, path: str) -> QgsMapLayer:
        raise NotImplementedError

class LoaderRegistry:
    def __init__(self):
        self._by_ext: Dict[str, BaseLoader] = {}

    def register(self, ext: str, loader: BaseLoader):
        if not ext.startswith("."):
            ext = "." + ext
        self._by_ext[ext.lower()] = loader

    def get_loader_for(self, path: str) -> BaseLoader:
        ext = os.path.splitext(path)[1].lower()
        if ext in self._by_ext:
            return self._by_ext[ext]
        raise LoaderError(f"No loader registered for extension: {ext}")

# singleton
loader_registry = LoaderRegistry()
