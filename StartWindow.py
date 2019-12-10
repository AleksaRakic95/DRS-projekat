from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon, QPixmap, QImage, QFont
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from Board import Board
import sys
from Controls import Controls, ControlsJump
from NumberOfPlayers import NumberOfPlayers


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()
        self.setFixedSize(800, 600)

        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(13);

        pybutton1 = QPushButton('New Game', self)
        pybutton1.clicked.connect(self.clickMethod1)
        pybutton1.resize(130, 50)
        pybutton1.move(340, 400)
        pybutton1.setStyleSheet("QPushButton { background-color: %s; "
                                "color: white; "
                                "font-family: Arcade Normal; font-weight: bold; font-size: 20px }" % QColor(0, 0, 0).
                                name())
        pybutton1.setFont(font)

        pybutton2 = QPushButton('Controls', self)
        pybutton2.clicked.connect(self.clickMethod2)
        pybutton2.resize(130, 50)
        pybutton2.move(340, 500)
        #pybutton2.setStyleSheet("QPushButton { background-color: %s}" % QColor(255, 255, 255).name())
        pybutton2.setStyleSheet("QPushButton { background-color: %s; "
                                "color: white; "
                                "font-family: Arcade Normal; font-weight: bold; font-size: 20px }" % QColor(0, 0,
                                                                                                            0).name())

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
        self.board.show()
        self.close()

    def clickMethod2(self):
        #print("Controls")
        #self.board.frame = QFrame()
        #self.board.frame = Controls()
        #self.board.show()
        self.frame = Controls()
        self.close()

        #self.nesto = Controls()