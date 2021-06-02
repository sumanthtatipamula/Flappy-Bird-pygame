# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['FlappyBird.py'],
             pathex=['C:\\Users\\TASUMANT\\Desktop\\FlappyBird'],
             binaries=[],
             datas=[('Assets/audio/*.wav', 'Assets/audio'),('Assets/images/*.png','Assets/images'),('Assets/fonts/*.TTF','Assets/fonts')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FlappyBird',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
