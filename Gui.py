from PyQt4 import QtCore, QtGui
from Encryptor import Encryptor
from Decryptor import Decryptor
import ImageProcessing as iP

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    file_path = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(830, 630)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.label_image = QtGui.QLabel(self.centralwidget)
        self.label_image.setText(_fromUtf8(""))
        self.label_image.setObjectName(_fromUtf8("label_image"))
        self.gridLayout.addWidget(self.label_image, 0, 0, 1, 1)
        if self.file_path != "":
            image = iP.get_image(self.file_path)
            pixmap = self.parse_image(image)
            self.label_image.setPixmap(pixmap)

        self.button_encrypt = QtGui.QPushButton(self.centralwidget)
        self.button_encrypt.setObjectName(_fromUtf8("button_encrypt"))
        self.gridLayout.addWidget(self.button_encrypt, 5, 0, 1, 1)
        self.button_encrypt.clicked.connect(self.encrypt)

        self.button_decrypt = QtGui.QPushButton(self.centralwidget)
        self.button_decrypt.setObjectName(_fromUtf8("button_decrypt"))
        self.gridLayout.addWidget(self.button_decrypt, 6, 0, 1, 1)
        self.button_decrypt.clicked.connect(self.decrypt)

        self.button_file = QtGui.QPushButton(self.centralwidget)
        self.button_file.setObjectName(_fromUtf8("button_file"))
        self.gridLayout.addWidget(self.button_file, 4, 0, 1, 1)
        self.button_file.clicked.connect(self.open_file)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.button_encrypt.setText(_translate("MainWindow", "Encrypt", None))
        self.button_decrypt.setText(_translate("MainWindow", "Decrypt", None))
        self.button_file.setText(_translate("MainWindow", "Choose file", None))

    def open_file(self):
        self.file_path = QtGui.QFileDialog.getOpenFileName(None, 'Open File')
        print(self.file_path)
        image = iP.get_image(self.file_path)
        pixmap = self.parse_image(image)
        self.label_image.setPixmap(pixmap)

    def encrypt(self):
        encryption = Encryptor(self.file_path)
        encryption.save_file()
        pixmap = self.parse_image(encryption.main_image)
        self.label_image.setPixmap(pixmap)
        self.file_path = encryption.encryption_path

    def parse_image(self, cvimage):
        height = cvimage.shape[0]
        width = cvimage.shape[1]
        bytes_per_line = 3 * width
        if len(cvimage.shape) > 2 :
            img = QtGui.QImage(cvimage.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
        else:
            img = QtGui.QImage(cvimage.data, width, height, QtGui.QImage.Format_Indexed8)
        pixmap = QtGui.QPixmap(img)
        pixmap = pixmap.scaledToWidth(500)
        return pixmap

    def decrypt(self):
        decryption = Decryptor(self.file_path)
        pixmap = self.parse_image(decryption.main_image)
        self.label_image.setPixmap(pixmap)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

