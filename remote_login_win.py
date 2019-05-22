"""处理远程登录信息"""
import qtawesome
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRegExp, pyqtSignal, Qt

from override import LineEdit, Button4ok, Button4cancel


class Login(QtWidgets.QDialog):
    # 自定义信号
    mySignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.initui()
        self.setWindowTitle('登录')
        self.setWindowIcon(qtawesome.icon('fa.sign-in', color='#ff5959'))
        self.setWindowModality(Qt.ApplicationModal)  # 对话窗口置顶
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)  # 去除不必要的按钮，仅QDialog
        self.setFixedSize(294, 241)

    def initui(self):
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.label_protocol = QtWidgets.QPushButton('文件协议')
        self.label_protocol.setObjectName('label')
        self.label_host = QtWidgets.QPushButton('主机地址')
        self.label_host.setObjectName('label')
        self.label_port = QtWidgets.QPushButton('端口')
        self.label_port.setObjectName('label')
        self.label_username = QtWidgets.QPushButton('用户名')
        self.label_username.setObjectName('label')
        self.label_password = QtWidgets.QPushButton('密码')
        self.label_password.setObjectName('label')
        self.pushbutton_login = Button4ok('登录')
        self.pushbutton_login.setFixedSize(72, 23)
        self.pushbutton_login.clicked.connect(self.sendsignal)
        self.pushbutton_close = Button4cancel('关闭')
        self.pushbutton_close.clicked.connect(self.close)
        self.combobox_protocol = QtWidgets.QComboBox()
        self.combobox_protocol.addItem('SFTP')
        self.linedit_host = LineEdit()
        self.linedit_host.setValidator(
            QtGui.QRegExpValidator(QRegExp(r'^[0-9]{2,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')))
        self.linedit_username = LineEdit()
        self.linedit_username.setValidator(QtGui.QRegExpValidator(QRegExp(r'^[a-zA-Z0-9_-]{3,16}')))
        self.linedit_password = LineEdit()
        self.linedit_password.setObjectName('password')
        self.linedit_password.setEchoMode(LineEdit.Password)
        self.qspinbox_port = QtWidgets.QSpinBox()
        self.qspinbox_port.setValue(22)
        self.main_layout.addWidget(self.label_protocol, 0, 0, 1, 4)
        self.main_layout.addWidget(self.combobox_protocol, 1, 0, 1, 4)
        self.main_layout.addWidget(self.label_host, 2, 0, 1, 4)
        self.main_layout.addWidget(self.label_port, 2, 4, 1, 4)
        self.main_layout.addWidget(self.linedit_host, 3, 0, 1, 4)
        self.main_layout.addWidget(self.qspinbox_port, 3, 4, 1, 2)
        self.main_layout.addWidget(self.label_username, 4, 0, 1, 4)
        self.main_layout.addWidget(self.label_password, 4, 4, 1, 4)
        self.main_layout.addWidget(self.linedit_username, 5, 0, 1, 4)
        self.main_layout.addWidget(self.linedit_password, 5, 4, 1, 4)
        self.main_layout.addWidget(self.pushbutton_login, 6, 4, 1, 2)
        self.main_layout.addWidget(self.pushbutton_close, 6, 6, 1, 2)
        """设置TAB顺序"""
        self.label_protocol.setFocusPolicy(Qt.NoFocus)
        self.label_host.setFocusPolicy(Qt.NoFocus)
        self.label_port.setFocusPolicy(Qt.NoFocus)
        self.label_username.setFocusPolicy(Qt.NoFocus)
        self.label_password.setFocusPolicy(Qt.NoFocus)
        self.combobox_protocol.setFocusPolicy(Qt.NoFocus)
        self.pushbutton_login.setFocusPolicy(Qt.NoFocus)
        self.pushbutton_close.setFocusPolicy(Qt.NoFocus)
        """设置样式表"""
        self.setStyleSheet('''
        QDialog{background:#FFFFFF;}
        QComboBox{font-size:11pd; color:#60607A;font-family:"Consolas";}
        QLineEdit{font-size:11pd; color:#60607A;font-family:"Consolas";}
        QSpinBox{font-size:11pd; color:#60607A;font-family:"Consolas";}
        QLineEdit#password{lineedit-password-character:9786;}
        QPushButton#label{border:none;background:none;font-family:"微软雅黑";text-align:left}''')

    def sendsignal(self):
        """连接到服务器"""
        self.close()
        message = {}
        message['protocol'] = self.combobox_protocol.currentText()
        message['host'] = self.linedit_host.text()
        message['port'] = int(self.qspinbox_port.text())
        message['username'] = self.linedit_username.text()
        message['password'] = self.linedit_password.text()
        self.mySignal.emit(message)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Login()
    win.show()
    sys.exit(app.exec_())