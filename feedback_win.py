import qtawesome
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from button_beautify import AnimationShadowEffect
from override import TextView


class FeedBack(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowOpacity(0.97)  # 窗口透明度
        self.setFixedSize(325, 215)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.mPos = None

    def init_ui(self):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.layout.addWidget(self.main_widget)
        self.content = TextView()
        self.content.setObjectName('content')
        self.label = QtWidgets.QLabel('意见反馈')
        self.send = QtWidgets.QPushButton(qtawesome.icon('fa.send', color='white'), '发送')
        self.send.setObjectName('button1')
        self.send.setFixedSize(72, 23)
        self.send_animation = AnimationShadowEffect(QColor('#87D087'), self.send)
        self.send.setGraphicsEffect(self.send_animation)
        self.send_animation.start()
        self.cancel = QtWidgets.QPushButton(qtawesome.icon('fa.window-close', color='#60607A'), '取消')
        self.cancel.setObjectName('button2')
        self.cancel.setFixedSize(72, 23)
        self.main_layout.addWidget(self.label, 0, 0, 1, 2)
        self.main_layout.addWidget(self.content, 1, 0, 3, 4)
        self.main_layout.addWidget(self.send, 4, 2, 1, 1)
        self.main_layout.addWidget(self.cancel, 4, 3, 1, 1)
        """添加阴影"""
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setBlurRadius(12)
        self.effect.setOffset(0, 0)
        self.effect.setColor(Qt.gray)
        self.setGraphicsEffect(self.effect)
        """样式表"""
        self.setStyleSheet('''
        QWidget{background:#F5F5F5;
        font-family:'Source Han Sans';
        border-top-left-radius:3px;
        border-top-right-radius:3px;
        border-bottom-left-radius:3px;
        border-bottom-right-radius:3px;
        border:gray}
        QTextEdit{
        background-color:#FFFFFF;
        border:1px solid #E6E6ED;
        border-top-left-radius:3px;
        border-top-right-radius:3px;
        border-bottom-left-radius:3px;
        border-bottom-right-radius:3px;}
        QLabel{background:none;border:none;font-size:10pd;font-family:"等线"}
        QPushButton#button1{border-style:none;padding:5px;border-radius:2px;background:#87D087;font-size:11pd;
            font-weight:bold;color:white;font-family:"Source Han Sans"}
        QPushButton#button2{border-style:none;padding:5px;border-radius:2px;border-color:gray;background:#FFFFFF;font-size:11pd;
            font-weight:bold;color:#60607A;font-family:"Source Han Sans"}
        QPushButton#button2:hover{background:#EFEFEF;border:1px solid #E6E6ED}''')
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标松开事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.move(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


if __name__ == '__main__':  # 本地文件测试
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = FeedBack()
    win.show()
    sys.exit(app.exec_())
