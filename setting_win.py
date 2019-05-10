"""设置界面"""
import qtawesome
from PyQt5 import QtWidgets


class Setting(QtWidgets.QFrame):
    def __int__(self):
        super().__init__()
        self.initui()
        self.setWindowTitle('设置')
        self.setWindowIcon(qtawesome.icon('fa.cog', color='pink'))

    def initui(self):
        self.main_layout = QtWidgets.QGridLayout()
        self.group1 = QtWidgets.QGroupBox('馈线柜断路器')
        self.group2 = QtWidgets.QGroupBox('进线柜断路器')
        self.button_save = QtWidgets.QPushButton('保存')
        self.button_save.clicked.connect(self.save_ini)
        self.button_cancle = QtWidgets.QPushButton('取消')
        self.button_cancle.clicked.connect(self.close)
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.group1, 0, 0, 3, 3)
        self.main_layout.addWidget(self.group2, 0, 3, 3, 3)
        self.main_layout.addWidget(self.button_save, 4, 1, 1, 2)
        self.main_layout.addWidget(self.button_cancle, 4, 4, 1, 1)

    def save_ini(self):
        pass


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Setting()
    win.show()
    sys.exit(app.exec_())
