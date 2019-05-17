# -*- mode: python -*-

block_cipher = None

a = Analysis(['startup.py'],
             pathex=['C:\\Users\\qiubin1\\PycharmProjects\\msg_report'],
             binaries=[],
             datas=[],
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
a.datas += (('log.txt', 'C:\\Users\\qiubin1\\PycharmProjects\\msg_report\\log.txt', 'LOG'),
            ('configure.ini', 'C:\\Users\\qiubin1\\PycharmProjects\\msg_report\\configure.ini', 'CONGIF'),
            ('icon/arrow2_feeder.svg', 'C:\\Users\\qiubin1\\PycharmProjects\\msg_report\\icon\\arrow2_feeder.svg',
             'ICO'),
            ('icon/arrow2_incoming.svg', 'C:\\Users\qiubin1\\PycharmProjects\\msg_report\\icon\\arrow2_incoming.svg',
             'ICO'),
            ('icon/main_win.svg', 'C:\\Users\qiubin1\\PycharmProjects\\msg_report\\icon\\main_win.svg',
             'ICO'),
            )
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Message',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='Message.ico', )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               version='1.0.0',
               name='startup')
