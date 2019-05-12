"""设置界面"""
import configparser

import qtawesome
from PyQt5 import QtWidgets
from  PyQt5.QtCore import Qt

from override import LineEdit1, Button4Setting, Button4ok, Button4cancel


class Setting(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initui()
        self.setWindowTitle('设置')
        self.setWindowIcon(qtawesome.icon('fa.cog', color='pink'))
        self.showini()

    def initui(self):
        self.setFixedSize(666, 193)
        self.main_layout = QtWidgets.QGridLayout()
        self.group1 = QtWidgets.QGroupBox('馈线柜断路器')
        self.group1_layout = QtWidgets.QGridLayout()
        self.group1.setLayout(self.group1_layout)
        self.group1_button_left1 = Button4Setting('分')
        self.group1_button_left2 = Button4Setting('合')
        self.group1_button_up1 = Button4Setting('FUN')
        self.group1_button_up2 = Button4Setting('INF')
        self.group1_button_up3 = Button4Setting('有效值')
        self.group1_line11 = LineEdit1()
        self.group1_line12 = LineEdit1()
        self.group1_line21 = LineEdit1()
        self.group1_line22 = LineEdit1()
        self.group1_line13 = LineEdit1()
        self.group1_line23 = LineEdit1()
        self.group1_layout.addWidget(self.group1_button_left1, 1, 0, 1, 1)
        self.group1_layout.addWidget(self.group1_button_left2, 2, 0, 1, 1)
        self.group1_layout.addWidget(self.group1_button_up1, 0, 1, 1, 1)
        self.group1_layout.addWidget(self.group1_button_up2, 0, 2, 1, 1)
        self.group1_layout.addWidget(self.group1_button_up3, 0, 3, 1, 1)
        self.group1_layout.addWidget(self.group1_line11, 1, 1, 1, 1)
        self.group1_layout.addWidget(self.group1_line12, 1, 2, 1, 1)
        self.group1_layout.addWidget(self.group1_line13, 1, 3, 1, 1)
        self.group1_layout.addWidget(self.group1_line21, 2, 1, 1, 1)
        self.group1_layout.addWidget(self.group1_line22, 2, 2, 1, 1)
        self.group1_layout.addWidget(self.group1_line23, 2, 3, 1, 1)
        self.group2 = QtWidgets.QGroupBox('进线柜断路器')
        self.group2_layout = QtWidgets.QGridLayout()
        self.group2.setLayout(self.group2_layout)
        self.group2_button_left1 = Button4Setting('分')
        self.group2_button_left2 = Button4Setting('合')
        self.group2_button_up1 = Button4Setting('FUN')
        self.group2_button_up2 = Button4Setting('INF')
        self.group2_button_up3 = Button4Setting('有效值')
        self.group2_line11 = LineEdit1()
        self.group2_line12 = LineEdit1()
        self.group2_line21 = LineEdit1()
        self.group2_line22 = LineEdit1()
        self.group2_line13 = LineEdit1()
        self.group2_line23 = LineEdit1()
        self.group2_layout.addWidget(self.group2_button_left1, 1, 4, 1, 1)
        self.group2_layout.addWidget(self.group2_button_left2, 2, 4, 1, 1)
        self.group2_layout.addWidget(self.group2_button_up1, 0, 5, 1, 1)
        self.group2_layout.addWidget(self.group2_button_up2, 0, 6, 1, 1)
        self.group2_layout.addWidget(self.group2_button_up3, 0, 7, 1, 1)
        self.group2_layout.addWidget(self.group2_line11, 1, 5, 1, 1)
        self.group2_layout.addWidget(self.group2_line12, 1, 6, 1, 1)
        self.group2_layout.addWidget(self.group2_line13, 1, 7, 1, 1)
        self.group2_layout.addWidget(self.group2_line21, 2, 5, 1, 1)
        self.group2_layout.addWidget(self.group2_line22, 2, 6, 1, 1)
        self.group2_layout.addWidget(self.group2_line23, 2, 7, 1, 1)
        self.button_save = Button4ok('保存')
        self.button_save.clicked.connect(self.save_ini)
        self.button_cancle = Button4cancel('取消')
        self.button_cancle.clicked.connect(self.close)
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.group1, 0, 0, 3, 4)
        self.main_layout.addWidget(self.group2, 0, 4, 3, 4)
        self.main_layout.addWidget(self.button_save, 3, 6, 1, 1)
        self.main_layout.addWidget(self.button_cancle, 3, 7, 1, 1)
        """设置TAB顺序"""
        self.group1_button_left1.setFocusPolicy(Qt.NoFocus)
        self.group1_button_left2.setFocusPolicy(Qt.NoFocus)
        self.group1_button_up1.setFocusPolicy(Qt.NoFocus)
        self.group1_button_up2.setFocusPolicy(Qt.NoFocus)
        self.group1_button_up3.setFocusPolicy(Qt.NoFocus)
        self.group2_button_left1.setFocusPolicy(Qt.NoFocus)
        self.group2_button_left2.setFocusPolicy(Qt.NoFocus)
        self.group2_button_up1.setFocusPolicy(Qt.NoFocus)
        self.group2_button_up2.setFocusPolicy(Qt.NoFocus)
        self.group2_button_up3.setFocusPolicy(Qt.NoFocus)
        self.button_save.setFocusPolicy(Qt.NoFocus)
        self.button_cancle.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet('''
            QFrame{background:#F5F5F5;}
            QGroupBox{font-family:"微软雅黑";}''')

    def save_ini(self):
        self.close()
        conf = configparser.ConfigParser()
        conf.read('configure.ini', 'utf-8')
        conf.set('馈线柜断路器分', 'FUN', self.group1_line11.text())
        conf.set('馈线柜断路器分', 'INF', self.group1_line12.text())
        conf.set('馈线柜断路器分', '有效值', self.group1_line13.text())
        conf.set('馈线柜断路器合', 'FUN', self.group1_line21.text())
        conf.set('馈线柜断路器合', 'INF', self.group1_line22.text())
        conf.set('馈线柜断路器合', '有效值', self.group1_line23.text())
        conf.set('进线柜断路器分', 'FUN', self.group2_line11.text())
        conf.set('进线柜断路器分', 'INF', self.group2_line12.text())
        conf.set('进线柜断路器分', '有效值', self.group2_line13.text())
        conf.set('进线柜断路器合', 'FUN', self.group2_line21.text())
        conf.set('进线柜断路器合', 'INF', self.group2_line22.text())
        conf.set('进线柜断路器合', '有效值', self.group2_line23.text())
        conf.write(open('configure.ini', 'r+', encoding='utf-8'))

    def showini(self):
        conf = configparser.ConfigParser()
        conf.read('configure.ini', 'utf-8')
        item1 = conf.items('馈线柜断路器分')
        self.group1_line11.setText(item1[0][1])
        self.group1_line12.setText(item1[1][1])
        self.group1_line13.setText(item1[2][1])
        item2 = conf.items('馈线柜断路器合')
        self.group1_line21.setText(item2[0][1])
        self.group1_line22.setText(item2[1][1])
        self.group1_line23.setText(item2[2][1])
        item3 = conf.items('进线柜断路器分')
        self.group2_line11.setText(item3[0][1])
        self.group2_line12.setText(item3[1][1])
        self.group2_line13.setText(item3[2][1])
        item4 = conf.items('进线柜断路器合')
        self.group2_line21.setText(item4[0][1])
        self.group2_line22.setText(item4[1][1])
        self.group2_line23.setText(item4[2][1])


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Setting()
    win.show()
    sys.exit(app.exec_())
