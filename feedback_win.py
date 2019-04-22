from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
import qtawesome, time


class FeedBack(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('意见反馈')
        self.setWindowIcon(qtawesome.icon('fa.rocket', color='grey'))
        self.setFixedSize(325, 215)
        # self.setWindowOpacity(0.95)  # 窗口透明度
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.label_content = QtWidgets.QPushButton(qtawesome.icon('fa.sticky-note', color='#272636'), '内容')
        self.label_content.setObjectName('label')
        self.label = QtWidgets.QPushButton('意见反馈')
        self.content = QtWidgets.QTextEdit()
        self.content.setObjectName('content')
        self.widget_1 = QtWidgets.QWidget()
        self.layout_1 = QtWidgets.QHBoxLayout()
        self.widget_1.setLayout(self.layout_1)
        self.send = QtWidgets.QPushButton(qtawesome.icon('fa.send', color='green'), '发送')
        self.send.setObjectName('button')
        self.cancel = QtWidgets.QPushButton(qtawesome.icon('fa.window-close', color='red'), '取消')
        self.cancel.setObjectName('button')
        self.main_layout.addWidget(self.content, 0, 0, 3, 4)
        self.main_layout.addWidget(self.widget_1, 3, 0, 1, 4)
        self.layout_1.addWidget(self.cancel, 3)
        self.layout_1.addWidget(self.send, 3)
        self.layout_1.setSpacing(35)
        """样式表"""
        self.main_widget.setStyleSheet('''
        background:#F5F5F5;
        font-family:'等线';''')
        self.label.setStyleSheet('''border:none;text-align:left''')  # 设置文字居左
        self.content.setStyleSheet('''
        background-color:#F5F5F5;
        border:1px solid gray;
        border-top-left-radius:5px;
        border-top-right-radius:5px;
        border-bottom-left-radius:5px;
        border-bottom-right-radius:5px;''')
        self.widget_1.setStyleSheet('''
        QPushButton#button{
        background-color:none;
        border:none;}''')
        self.send.setStyleSheet('''
        QPushButton#button:hover{
        color:green;
        font: 75 10pt "微软雅黑";}''')
        self.cancel.setStyleSheet('''
        QPushButton#button:hover{
        color:red;
        font: 75 10pt "微软雅黑";}''')
        """动作"""
        self.cancel.clicked.connect(self.close)
        self.send.clicked.connect(self.savelog)

    def savelog(self):
        file = open('.\\log.txt', mode='a', encoding='utf-8')
        file.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n')
        file.write(self.content.toPlainText() + '\n')
        file.write('***********************************************\n')
        file.close()
        self.close()


if __name__ == '__main__':  # 本地文件测试
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = FeedBack()
    win.show()
    sys.exit(app.exec_())
