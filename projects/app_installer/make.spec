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
    name='App Installer',
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
    name='App Installer',
)
app = BUNDLE(
    coll,
    name='App Installer.app',
    icon='icon.icns',
    bundle_identifier='com.need4swede.AppInstaller',
    info_plist={
      'CFBundleName': 'AppInstaller',
      'CFBundleDisplayName': 'AppInstaller',
      'CFBundleVersion': '1.0',
      'CFBundleShortVersionString': '1.0',
      'NSRequiresAquaSystemAppearance': 'No',
      'NSHighResolutionCapable': 'True',
    },
)
