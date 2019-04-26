""""复写以适应需求"""
from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome


class Button4Icon(QtWidgets.QPushButton):
    """复写QPushButton为小按钮"""

    def __init__(self, icon: str):
        super().__init__()
        self.btn_icon = icon
        self.setIcon(qtawesome.icon(self.btn_icon, color='white'))  # 初始图标颜色

    def enterEvent(self, a0: QtCore.QEvent):
        """复写鼠标进入事件"""
        if self.enterEvent:
            self.setIcon(qtawesome.icon(self.btn_icon, color='#e2598b'))

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
                background:#243040;color:#F49900;}
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
