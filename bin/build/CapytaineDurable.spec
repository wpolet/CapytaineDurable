# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:/Users/William/Documents/GitHub/1920_INFOB318_Ca--py--taineDurable/code/main.py'],
             pathex=['C:/Users/William/Documents/GitHub/1920_INFOB318_Ca--py--taineDurable/bin/build'],
             binaries=[],
             datas=[('C:/Users/William/Documents/GitHub/1920_INFOB318_Ca--py--taineDurable/code/img', 'img'), ('C:/Users/William/Documents/GitHub/1920_INFOB318_Ca--py--taineDurable/code/maps', 'maps'), ('C:/Users/William/Documents/GitHub/1920_INFOB318_Ca--py--taineDurable/code/media', 'media')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
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
          name='CapytaineDurable',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CapytaineDurable')
