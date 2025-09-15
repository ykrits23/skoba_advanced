# hook-qgis-runtime.py
import os, sys

QGIS_PREFIX = r"C:\Program Files\QGIS 3.34.8\apps\qgis-ltr"
QGIS_BIN = r"C:\Program Files\QGIS 3.34.8\bin"
QGIS_PYTHON = os.path.join(QGIS_PREFIX, "python")
QGIS_SITE = r"C:\Program Files\QGIS 3.34.8\apps\Python312\Lib\site-packages"

os.environ['PATH'] = QGIS_BIN + os.pathsep + os.environ.get('PATH', '')
os.environ['QGIS_PREFIX_PATH'] = QGIS_PREFIX

if QGIS_PYTHON not in sys.path:
    sys.path.insert(0, QGIS_PYTHON)
if QGIS_SITE not in sys.path:
    sys.path.insert(0, QGIS_SITE)
