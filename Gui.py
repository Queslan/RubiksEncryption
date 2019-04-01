from PyQt4 import QtCore, QtGui
from Encryptor import Encryptor
from Decryptor import Decryptor
from Statistics import histogram
import ImageProcessing as iP
import os

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

        self.label_image = QtGui.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(10, 0, 480, 480))
        self.label_image.setMinimumSize(QtCore.QSize(480, 480))
        self.label_image.setText(_fromUtf8(""))
        self.label_image.setObjectName(_fromUtf8("label_image"))
        if self.file_path != "":
            image = iP.get_image(self.file_path)
            pixmap = self.parse_image(image, 500)
            self.label_image.setPixmap(pixmap)

        self.button_encrypt = QtGui.QPushButton(self.centralwidget)
        self.button_encrypt.setGeometry(QtCore.QRect(300, 540, 100, 50))
        self.button_encrypt.setObjectName(_fromUtf8("button_encrypt"))
        self.button_encrypt.clicked.connect(self.encrypt)

        self.button_decrypt = QtGui.QPushButton(self.centralwidget)
        self.button_decrypt.setGeometry(QtCore.QRect(500, 540, 100, 50))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_decrypt.sizePolicy().hasHeightForWidth())

        self.button_decrypt.setSizePolicy(sizePolicy)
        self.button_decrypt.setObjectName(_fromUtf8("button_decrypt"))
        self.button_decrypt.clicked.connect(self.decrypt)

        self.button_chooseFile = QtGui.QPushButton(self.centralwidget)
        self.button_chooseFile.setGeometry(QtCore.QRect(100, 540, 100, 50))
        self.button_chooseFile.setObjectName(_fromUtf8("button_chooseFile"))
        self.button_chooseFile.clicked.connect(self.open_file)

        self.label_histogram = QtGui.QLabel(self.centralwidget)
        self.label_histogram.setGeometry(QtCore.QRect(500, 200, 320, 240))
        self.label_histogram.setMinimumSize(QtCore.QSize(320, 240))
        self.label_histogram.setText(_fromUtf8(""))
        self.label_histogram.setObjectName(_fromUtf8("label_histogram"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 21))
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
        self.button_chooseFile.setText(_translate("MainWindow", "Choose file", None))

    def open_file(self):
        self.file_path = QtGui.QFileDialog.getOpenFileName(None, 'Open File')
        image = iP.get_image(self.file_path)
        pixmap = self.parse_image(image, 500)
        self.label_image.setPixmap(pixmap)
        self.makeHistogram()

    def encrypt(self):
        encryption = Encryptor(self.file_path)
        encryption.save_file()
        parsed_image = self.parse_image(encryption.main_image, 500)
        self.label_image.setPixmap(parsed_image)
        self.file_path = encryption.encryption_path
        self.makeHistogram()

    def parse_image(self, cvimage, size, number = 0):
        height = cvimage.shape[0]
        width = cvimage.shape[1]
        bytes_per_line = 3 * width
        if len(cvimage.shape) > 2 and number == 0:
            img = QtGui.QImage(cvimage.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
        else:
            img = QtGui.QImage(cvimage.data, width, height, QtGui.QImage.Format_Indexed8)
        parsed_image = QtGui.QPixmap(img)
        #pixmap = pixmap.scaledToWidth(size)
        return parsed_image

    def decrypt(self):
        decryption = Decryptor(self.file_path)
        decryption.save_file()
        parsed_image = self.parse_image(decryption.main_image, 500)
        self.label_image.setPixmap(parsed_image)
        self.file_path = decryption.decryption_path
        self.makeHistogram()

    def makeHistogram(self):
        image = iP.get_image(self.file_path)
        histogram(image)
        histogram_pixmap = QtGui.QPixmap('result/histogram.png').scaledToWidth(320)
        self.label_histogram.setPixmap(histogram_pixmap)


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

