"""显示服务器文件列表并下载"""
import paramiko
import qtawesome
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

from button_beautify import AnimationShadowEffect


class File_dowload(QtWidgets.QFrame):
    def __init__(self, remote_path=None, filelist=[], transport=None, statusbar=None):
        super().__init__()
        self.localpath = r'C:\*.txt'
        self.remote_path = remote_path
        self.filelist = filelist
        self.transport = transport
        self.statusbar = statusbar
        self.initui()

    def initui(self):
        self.setWindowTitle('download')
        self.setWindowIcon(qtawesome.icon('fa.cloud-download', color='black'))
        self.main_layout = QtWidgets.QGridLayout()
        self.list_widget = QtWidgets.QListWidget()
        self.setFixedSize(300, 600)
        self.button_cancel = QtWidgets.QPushButton('取消')
        self.button_cancel.setFixedWidth(50)
        self.button_cancel.setObjectName('button1')
        self.button_cancel.clicked.connect(self.close)
        self.button_ok = QtWidgets.QPushButton('下载')
        self.button_ok.setFixedWidth(50)
        self.button_ok_animation = AnimationShadowEffect(QColor('#87D087'), self.button_ok)
        self.button_ok.setGraphicsEffect(self.button_ok_animation)
        self.button_ok_animation.start()
        self.button_ok.setObjectName('button2')
        self.button_ok.clicked.connect(self.dowload)
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.list_widget, 0, 0, 5, 6)
        self.main_layout.addWidget(self.button_ok, 5, 1, 1, 1)
        self.main_layout.addWidget(self.button_cancel, 5, 4, 1, 1)
        self.list_widget.addItems(self.filelist)
        """设置样式表"""
        self.setStyleSheet('''
                QFrame{background:#FFFFFF;}
                QPushButton#button2{border-style:none;padding:5px;border-radius:2px;background:#87D087;font-size:11pd;
                    font-weight:bold;color:white;font-family:"Source Han Sans"}
                QPushButton#button1{border-style:none;padding:5px;border-radius:2px;background:#FFFFFF;font-size:11pd;
                    font-weight:bold;color:#60607A;font-family:"Source Han Sans"}
                QPushButton#button1:hover{background:#EFEFEF;border:1px solid #E6E6ED;padding:1px}
                QPushButton#label{border:none;background:none;font-family:"Source Han Sans";font-size:11pd;font-weight:487;text-align:left}''')

    def dowload(self):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.currentindex = self.list_widget.currentRow()
        sftp.get(remotepath=self.remote_path + self.filelist[self.currentindex], localpath=self.localpath)  # 下载文件,目录待定
        self.transport.close()
        self.close()
        self.statusbar.showMessage('已下载至：' + self.localpath)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = File_dowload()
    win.show()
    sys.exit(app.exec_())
