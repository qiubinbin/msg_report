import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from main_win import Msg_als

app = QtWidgets.QApplication(sys.argv)
splash = QtWidgets.QSplashScreen(QtGui.QPixmap('icon/ml.bmp'))
splash.show()
QtWidgets.qApp.processEvents()
win = Msg_als()
win.show()
splash.close()
sys.exit(app.exec_())
