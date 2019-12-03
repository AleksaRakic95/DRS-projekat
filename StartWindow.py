from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon, QPixmap, QImage
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from Board import  Board
import sys


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()

        pybutton1 = QPushButton('Play', self)
        pybutton1.clicked.connect(self.clickMethod1)
        pybutton1.resize(100, 50)
        pybutton1.move(350, 400)
        pybutton1.setStyleSheet("QPushButton { background-color: %s}" % QColor(255, 255, 255).name())

        pybutton2 = QPushButton('Controls', self)
        pybutton2.clicked.connect(self.clickMethod2)
        pybutton2.resize(100, 50)
        pybutton2.move(350, 500)
        pybutton2.setStyleSheet("QPushButton { background-color: %s}" % QColor(255, 255, 255).name())


        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.label = QLabel(self)
        pixmapFull = QPixmap('Asset/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(800, 300, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def clickMethod1(self):
        self.board = Board()
        self.board.show()
        self.close()

    def clickMethod2(self):
        print("Controls")
