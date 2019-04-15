from Gui import Ui_MainWindow
import os
from PyQt4 import QtGui


if __name__ == "__main__":
    import sys

    if not os.path.exists("result"):
        os.makedirs("result")
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
