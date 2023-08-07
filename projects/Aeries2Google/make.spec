# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Aeries2Google',
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
    icon='icon.icns',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Aeries2Google',
)
app = BUNDLE(
    coll,
    name='Aeries2Google.app',
    icon='icon.icns',
    bundle_identifier='com.need4swede.aeries2google',
    info_plist={
      'CFBundleName': 'Aeries2Google',
      'CFBundleDisplayName': 'Aeries2Google',
      'CFBundleVersion': '1.0',
      'CFBundleShortVersionString': '1.0',
      'NSRequiresAquaSystemAppearance': 'No',
      'NSHighResolutionCapable': 'True',
    },
)
