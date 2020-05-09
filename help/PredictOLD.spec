# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
from PyInstaller.utils.hooks import collect_submodules
import sys

sys.setrecursionlimit(2000)


a = Analysis(['C:\\Users\\Pranav Devarinti\\OneDrive - Cobb County School District\\SPV6\\Predict.py'],
             pathex=['C:\\Users\\Pranav Devarinti\\OneDrive - Cobb County School District\\SPV6'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn'],
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
          name='Predict',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
