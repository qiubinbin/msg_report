import sys
import time

from PyQt5 import QtWidgets, QtGui,QtSvg

from main_win import Msg_als

app = QtWidgets.QApplication(sys.argv)
start=QtSvg.QSvgWidget('icon/ml.svg')
splash = QtWidgets.QSplashScreen(QtGui.QPixmap('icon/ml.svg'))  # 使用bmp无法使用α通道
splash.show()
QtWidgets.qApp.processEvents()
win = Msg_als()
time.sleep(0.7)
win.show()
splash.close()
sys.exit(app.exec_())
