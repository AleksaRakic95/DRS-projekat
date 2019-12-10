from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon, QPixmap, QImage, QFont
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from Board import  Board
from NumberOfPlayers import NumberOfPlayers
import sys
from Controls import Controls, ControlsJump


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()

        pybutton1 = QPushButton('New Game', self)
        pybutton1.clicked.connect(self.clickMethod1)
        pybutton1.resize(180, 50)
        pybutton1.move(310, 400)

        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(15)
        font.bold()

        pybutton1.setStyleSheet("QPushButton:!hover { background-color: black; color: white; }"
                                "QPushButton:hover { background-color: black; color: red; }")
        pybutton1.setFont(font)

        pybutton2 = QPushButton('Controls', self)
        pybutton2.clicked.connect(self.clickMethod2)
        pybutton2.resize(160, 50)
        pybutton2.move(320, 500)

        pybutton2.setStyleSheet("QPushButton:!hover { background-color: black; color: white; }"
                                "QPushButton:hover { background-color: black; color: red; }")
        pybutton2.setFont(font)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.label = QLabel(self)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(800, 300, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def clickMethod1(self):
        self.board = NumberOfPlayers()
        self.close()

    def clickMethod2(self):
        self.frame = Controls()
        self.close()