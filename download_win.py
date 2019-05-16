"""显示服务器文件列表并下载"""
import paramiko
import qtawesome
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt

from override import Button4ok, Button4cancel


class OpenTip(QtWidgets.QDialog):
    mySignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initui()
        self.setWindowModality(Qt.ApplicationModal)  # 对话窗口置顶
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)  # 去除不必要的按钮

    def initui(self):
        self.setWindowIcon(qtawesome.icon('fa.exclamation-circle', color='red'))
        self.setWindowTitle('下载完成，是否立即打开？')
        self.setFixedSize(316, 50)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.button_open = Button4ok('打开')
        self.button_cancle = Button4cancel('取消')
        self.button_cancle.setToolTip('稍后可手动打开')
        self.button_cancle.setObjectName('cancle')
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.button_open)
        self.main_layout.addWidget(self.button_cancle)
        self.button_cancle.clicked.connect(self.cancle)
        self.button_open.clicked.connect(self.openfile)
        self.setStyleSheet('''
        QDialog{background:#FFFFFF;}''')

    def cancle(self):
        self.close()
        self.mySignal.emit(False)

    def openfile(self):
        self.close()
        self.mySignal.emit(True)


class File_dowload(QtWidgets.QDialog):
    mySignal = pyqtSignal(str)

    def __init__(self, remote_path=None, filelist=[], transport=None, statusbar=None):
        super().__init__()
        self.localpath = r'C:/Users/qiubi/Desktop/'
        self.remote_path = remote_path
        self.filelist = filelist
        self.transport = transport
        self.statusbar = statusbar
        self.setWindowModality(Qt.ApplicationModal)  # 对话窗口置顶
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)  # 去除不必要的按钮
        self.initui()

    def initui(self):
        self.setWindowTitle('download')
        self.setWindowIcon(qtawesome.icon('fa.cloud-download', color='#7189bf'))
        self.main_layout = QtWidgets.QGridLayout()
        self.list_widget = QtWidgets.QListWidget()
        self.setFixedSize(300, 600)
        self.button_cancel = Button4cancel('取消')
        self.button_cancel.setFixedWidth(50)
        self.button_cancel.clicked.connect(self.close)
        self.button_ok = Button4ok('下载')
        self.button_ok.setFixedWidth(50)
        self.button_ok.clicked.connect(self.dowload)
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.list_widget, 0, 0, 5, 6)
        self.main_layout.addWidget(self.button_ok, 5, 1, 1, 1)
        self.main_layout.addWidget(self.button_cancel, 5, 4, 1, 1)
        self.list_widget.addItems(self.filelist)
        """设置TAB顺序"""
        self.button_ok.setFocusPolicy(Qt.NoFocus)
        self.button_cancel.setFocusPolicy(Qt.NoFocus)
        """设置样式表"""
        self.setStyleSheet('''
                QDialog{background:#FFFFFF;}
                QPushButton#label{border:none;background:none;font-family:"Source Han Sans";font-size:11pd;font-weight:487;text-align:left}''')

    def dowload(self):
        self.currentindex = self.list_widget.currentRow()
        path = QtWidgets.QFileDialog.getExistingDirectory(self, '打开', 'C:\\')
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.get(remotepath=self.remote_path + self.filelist[self.currentindex],
                 localpath=path + '/' + self.filelist[self.currentindex])  # 下载文件,目录待定
        self.transport.close()
        self.close()
        self.statusbar.showMessage('已保存至：' + self.localpath)
        self.mySignal.emit(path + '/')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = File_dowload()
    win.show()
    sys.exit(app.exec_())
