# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

block_cipher = None

extra_datas = []
extra_binaries = []
extra_hiddenimports = [
    'uvicorn.logging',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'uvicorn.lifespan.off',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.http.httptools_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.websockets.wsproto_impl',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.loops.asyncio',
]

for pkg in ['whisperx', 'torch', 'torchaudio', 'faster_whisper', 'ctranslate2', 'transformers', 'torchcodec', 'pyannote.audio', 'pyannote.core', 'pyannote.pipeline', 'speechbrain', 'imageio', 'imageio_ffmpeg', 'moviepy']:
    try:
        tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all(pkg)
        extra_datas += tmp_datas
        extra_binaries += tmp_binaries
        extra_hiddenimports += tmp_hiddenimports
    except Exception:
        pass

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=extra_binaries,
    datas=extra_datas,
    hiddenimports=extra_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='modsquad-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='modsquad-backend',
)
