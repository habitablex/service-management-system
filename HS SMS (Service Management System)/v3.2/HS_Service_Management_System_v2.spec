# PyInstaller spec for HS Service Management System v3.2
# Build on Windows with: pyinstaller HS_Service_Management_System_v2.spec

block_cipher = None

a = Analysis(
    ['HS_Service_Management_System_v2.py'],
    pathex=[],
    binaries=[],
    datas=[('README_CLIENT.txt', '.'), ('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HS_Service_Management_System_v3_2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/hs_sms_icon.ico',
)
