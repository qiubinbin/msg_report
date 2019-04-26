from PyQt5 import QtWidgets
import qtawesome


class Login(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initui()
        self.setWindowTitle('登录')
        self.setWindowIcon(qtawesome.icon('fa.sign-in'))
        self.setWindowOpacity(0.95)  # 窗口透明度
        self.setFixedSize(294, 241)

    def initui(self):
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.label_protocol = QtWidgets.QPushButton('文件协议')
        self.label_protocol.setObjectName('label')
        self.label_host = QtWidgets.QPushButton('主机名')
        self.label_host.setObjectName('label')
        self.label_port = QtWidgets.QPushButton('端口')
        self.label_port.setObjectName('label')
        self.label_username = QtWidgets.QPushButton('用户名')
        self.label_username.setObjectName('label')
        self.label_password = QtWidgets.QPushButton('密码')
        self.label_password.setObjectName('label')
        self.pushbutton_login = QtWidgets.QPushButton('登录')
        self.pushbutton_login.setFixedSize(72, 23)
        self.pushbutton_login.setObjectName('button1')
        self.pushbutton_close = QtWidgets.QPushButton('关闭')
        self.pushbutton_close.setObjectName('button2')
        self.combobox_protocol = QtWidgets.QComboBox()
        self.linedit_host = QtWidgets.QLineEdit()
        self.linedit_username = QtWidgets.QLineEdit()
        self.linedit_password = QtWidgets.QLineEdit()
        self.qspinbox_port = QtWidgets.QSpinBox()
        self.main_layout.addWidget(self.label_protocol, 0, 0, 1, 4)
        self.main_layout.addWidget(self.combobox_protocol, 1, 0, 1, 4)
        self.main_layout.addWidget(self.label_host, 2, 0, 1, 4)
        self.main_layout.addWidget(self.label_port, 2, 4, 1, 4)
        self.main_layout.addWidget(self.linedit_host, 3, 0, 1, 4)
        self.main_layout.addWidget(self.qspinbox_port, 3, 4, 1, 4)
        self.main_layout.addWidget(self.label_username, 4, 0, 1, 4)
        self.main_layout.addWidget(self.label_password, 4, 4, 1, 4)
        self.main_layout.addWidget(self.linedit_username, 5, 0, 1, 4)
        self.main_layout.addWidget(self.linedit_password, 5, 4, 1, 4)
        self.main_layout.addWidget(self.pushbutton_login, 6, 4, 1, 2)
        self.main_layout.addWidget(self.pushbutton_close, 6, 6, 1, 2)
        """设置样式表"""
        self.setStyleSheet('''
        QFrame{background:#F5F5F5;}
        QPushButton#button1{border-style:none;padding:5px;border-radius:2px;background:#87D087;font-size:11pd;
            font-weight:bold;color:white;font-family:"Source Han Sans"}
        QPushButton#button2{border-style:none;padding:5px;border-radius:2px;background:#FFFFFF;font-size:11pd;
            font-weight:bold;color:#60607A;font-family:"Source Han Sans"}
        QPushButton#button2:hover{background:#EFEFEF}''')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Login()
    win.show()
    sys.exit(app.exec_())
