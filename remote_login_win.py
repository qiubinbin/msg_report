import qtawesome
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRegExp, pyqtSignal
from PyQt5.QtGui import QColor

from button_beautify import AnimationShadowEffect
from override import LineEdit


class Login(QtWidgets.QFrame):
    # 自定义信号
    mySignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.initui()
        self.setWindowTitle('登录')
        self.setWindowIcon(qtawesome.icon('fa.sign-in'))
        # self.setWindowOpacity(0.95)  # 窗口透明度
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
        self.pushbutton_login = QtWidgets.QPushButton('登录')
        self.pushbutton_login.setFixedSize(72, 23)
        self.pushbutton_login_animation = AnimationShadowEffect(QColor('#87D087'), self.pushbutton_login)
        self.pushbutton_login.setGraphicsEffect(self.pushbutton_login_animation)
        self.pushbutton_login_animation.start()
        self.pushbutton_login.setObjectName('button1')
        self.pushbutton_login.clicked.connect(self.sendsignal)
        self.pushbutton_close = QtWidgets.QPushButton('关闭')
        self.pushbutton_close.clicked.connect(self.close)
        self.pushbutton_close.setObjectName('button2')
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
        """设置样式表"""
        self.setStyleSheet('''
        QFrame{background:#F5F5F5;}
        QLineEdit#password{lineedit-password-character:9786}
        QPushButton#button1{border-style:none;padding:5px;border-radius:2px;background:#87D087;font-size:11pd;
            font-weight:bold;color:white;font-family:"Source Han Sans"}
        QPushButton#button2{border-style:none;padding:5px;border-radius:2px;background:#FFFFFF;font-size:11pd;
            font-weight:bold;color:#60607A;font-family:"Source Han Sans"}
        QPushButton#button2:hover{background:#EFEFEF;border:1px solid #E6E6ED;padding:1px}
        QPushButton#label{border:none;background:none;font-family:"Source Han Sans";font-size:11pd;font-weight:487;text-align:left}''')

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
