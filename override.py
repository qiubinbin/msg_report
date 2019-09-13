""""复写以适应需求"""
import qtawesome
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

from button_beautify import AnimationShadowEffect


class WebView(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.bw = QWebEngineView()
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.bw)
        self.setui()

    def sethtml(self, str='hahah'):
        self.bw.setHtml(str)

    def setui(self):
        self.setStyleSheet('''
            border:2px solid #698FBF;
            padding:0px;
            margin:0px;
            border-radius: 8px;''')


class Button4Icon(QtWidgets.QPushButton):
    """复写QPushButton为小按钮"""

    def __init__(self, icon: str):
        super().__init__()
        self.btn_icon = icon
        self.setIcon(qtawesome.icon(self.btn_icon, color='white'))  # 初始图标颜色

    def enterEvent(self, a0: QtCore.QEvent):
        """复写鼠标进入事件"""
        if self.enterEvent:
            self.setIcon(qtawesome.icon(self.btn_icon, color='#01d28e'))

    def leaveEvent(self, a0: QtCore.QEvent):
        """复写鼠标离开事件"""
        if self.leaveEvent:
            self.setIcon(qtawesome.icon(self.btn_icon, color='white'))


class TextView(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.initui()
        self.setStyleSheet('''
        selection-color:#99CA90;
        selection-background-color:#273141''')

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent):
        menu = QtWidgets.QMenu()
        action_paste = QtWidgets.QAction(qtawesome.icon('fa.clipboard', color='black'), '粘贴')
        action_clear = QtWidgets.QAction(qtawesome.icon('fa.trash', color='black'), '清空')
        action_paste.setShortcut('Ctrl+V')
        menu.setStyleSheet('''QMenu{border:none;background:none;color:black;}
        QMenu:item:selected:enabled{background:#E8EAED}
        QMenu::item:selected:!enabled{background:transparent;}
        QMenu::separator{width:1px;}''')
        if not self.isReadOnly():
            menu.addAction(action_paste)
            menu.addAction(action_clear)
            action_clear.triggered.connect(self.clear)
            action_paste.triggered.connect(self.paste)
        else:
            pass
        menu.exec_(QtGui.QCursor.pos())

    def initui(self):
        self.verticalScrollBar().setStyleSheet('''
                QScrollBar:vertical{padding-top:18px;padding-bottom:18px;
                background-color:white;}
                QScrollBar:handle:vertical{border:none}
                QScrollBar:add-line:vertical{height:17px;color:#F49900;background:#243040;}
                QScrollBar:sub-line:vertical{height:17px;color:#F49900;background:#243040;}
                QScrollBar:add-page:vertical{background:#F0F0F0;}
                QScrollBar:sub-page:vertical{background:#F0F0F0;}''')


class LineEdit(QtWidgets.QLineEdit):
    """复写qlineedit"""

    def __int__(self):
        super().__init__()
        self.setStyleSheet('''
        selection-color:#99CA90;
        selection-background-color:#273141''')

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent):
        """重定义右键菜单"""
        menu = QtWidgets.QMenu()
        action_paste = QtWidgets.QAction(qtawesome.icon('fa.clipboard', color='black'), '粘贴')
        action_clear = QtWidgets.QAction(qtawesome.icon('fa.trash', color='black'), '清空')
        action_paste.setShortcut('Ctrl+V')
        menu.setStyleSheet('''QMenu{border:none;background:none;color:black;}
                        QMenu:item:selected:enabled{background:#E8EAED}
                        QMenu::item:selected:!enabled{background:transparent;}
                        QMenu::separator{width:1px;}''')
        menu.addAction(action_paste)
        menu.addAction(action_clear)
        action_clear.triggered.connect(self.clear)
        action_paste.triggered.connect(self.paste)
        menu.exec_(QtGui.QCursor.pos())


class Button4Setting(QtWidgets.QPushButton):
    """复写qpushbutton"""

    def __init__(self, content):
        super().__init__(content)
        self.setStyleSheet('''font-family:"微软雅黑";border:none''')
        self.setFixedWidth(70)


class LineEdit1(QtWidgets.QLineEdit):
    """复写qlineedit"""

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setValidator(QtGui.QRegExpValidator(QRegExp(r'^[0-9A-E]{2}')))
        self.setStyleSheet('''font-family:"Consolas";''')
        self.setFixedWidth(70)


class Button4ok(QtWidgets.QPushButton):
    def __init__(self, content):
        super().__init__(content)
        self.animation = AnimationShadowEffect(QColor('#87D087'), self)
        self.setGraphicsEffect(self.animation)
        self.animation.start()
        self.setStyleSheet('''
        QPushButton{border-style:none;padding:5px;background:#87D087;font-size:11pd;
            font-weight:bold;color:white;font-family:"Source Han Sans"}''')


class Button4cancel(QtWidgets.QPushButton):
    def __init__(self, content):
        super().__init__(content)
        self.setStyleSheet('''
        QPushButton{border-style:none;padding:5px;background:#F4F4F4;font-size:11pd;
            font-weight:bold;color:#60607A;font-family:"Source Han Sans"}
        QPushButton:hover{background:#E5F1FB;border:1px solid #0078D7;padding:1px}''')
