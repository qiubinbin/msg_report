from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')
include = ['sip']
py2exe_options = {  # py2exe中的options字典
    "py2exe": {
        "compressed": 1,  # 压缩
        "optimize": 2,
        "bundle_files": 1,  # 所有文件打包成一个 exe 文件
        "includes": include,
        "dll_excludes": ["MSVCR100.dll"]}
}

setup(
    windows=['startup.py',
             'button_beautify.py',
             'configure.ini',
             'download_win.py',
             'feedback_win.py',
             'IEC103.py',
             'main_win.py',
             'override.py',
             'remote_login_win.py',
             'setting_win.py', ],
    version='1.0.0',
    options=py2exe_options,
    name='报文',
    zipfile=None,
    console=[{"script": 'startup.py', "icon": [(1, u"图标.svg")]}],
    data_files=[('icon', ['C:/Users/qiubin1/PycharmProjects/msg_report/icon/icon/arrow2_feeder.svg']),
                ('icon', ['C:/Users/qiubin1/PycharmProjects/msg_report/icon/icon/icon/arrow2_incoming.svg']),
                ('icon', ['C:/Users/qiubin1/PycharmProjects/msg_report/icon/icon/icon/icon/图标.svg']),
                ('txt', ['C:/Users/qiubin1/PycharmProjects/msg_report/log.txt']),
                ('txt', ['C:/Users/qiubin1/PycharmProjects/msg_report/记录.txt']), ]
)
