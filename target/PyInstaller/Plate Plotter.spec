# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/coltongarelli/PycharmProjects/PlateMapper/src/main/python/app/main_window.py'],
             pathex=['/Users/coltongarelli/PycharmProjects/PlateMapper/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Users/coltongarelli/anaconda3/envs/PlatePlotter/lib/python3.7/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/Users/coltongarelli/PycharmProjects/PlateMapper/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Plate Plotter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/coltongarelli/PycharmProjects/PlateMapper/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='Plate Plotter')
app = BUNDLE(coll,
             name='Plate Plotter.app',
             icon='/Users/coltongarelli/PycharmProjects/PlateMapper/target/Icon.icns',
             bundle_identifier=None)
