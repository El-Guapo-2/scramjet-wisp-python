# PyInstaller build configuration for the console-mode Windows executable.

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


root = Path(SPECPATH)
public = root / "packages" / "create-proxy-app" / "templates" / "default" / "public"

a = Analysis(
    [str(root / "python_server.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(public), "scramjet_public")],
    hiddenimports=(
        collect_submodules("wisp")
        + collect_submodules("websockets")
        + collect_submodules("asyncudp")
        + collect_submodules("python_socks")
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="scramjet-python-server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
