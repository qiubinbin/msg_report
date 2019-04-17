from PyQt5 import QtWidgets
import sys
from main_win import Msg_als

app = QtWidgets.QApplication(sys.argv)
win = Msg_als()
win.show()
sys.exit(app.exec_())
