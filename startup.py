import sys
import time

from PyQt5 import QtWidgets, QtGui

from main_win import Msg_als

app = QtWidgets.QApplication(sys.argv)
splash = QtWidgets.QSplashScreen(QtGui.QPixmap('icon/ml.bmp'))
splash.show()
QtWidgets.qApp.processEvents()
win = Msg_als()
time.sleep(0.7)
win.show()
splash.close()
sys.exit(app.exec_())
