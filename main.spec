# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:\\Program Files\\QGIS 3.34.8\\apps\\qgis-ltr\\python', 'C:\\Program Files\\QGIS 3.34.8\\apps\\Qt5\\bin'],
    binaries=[],
    datas=[('C:\\Program Files\\QGIS 3.34.8\\apps\\Qt5\\plugins', 'plugins'), ('C:\\Program Files\\QGIS 3.34.8\\apps\\qgis-ltr\\resources', 'resources'), ('C:\\Program Files\\QGIS 3.34.8\\apps\\gdal', 'gdal')],
    hiddenimports=['qgis._core'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
