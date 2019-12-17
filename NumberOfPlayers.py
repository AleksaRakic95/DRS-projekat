from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon, QPixmap, QImage, QFont
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from OnePlayer import OnePlayer
from TwoPlayers import TwoPlayers
import sys


class NumberOfPlayers(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()
        self.setFixedSize(800, 600)

        self.textLabel = QLabel(self)
        self.textLabel.move(100, 300)
        fontLabel = QFont()
        fontLabel.setFamily("Arcade Normal")
        fontLabel.setPointSize(20)
        self.textLabel.setStyleSheet('color: white;')
        self.textLabel.setFont(fontLabel)
        self.textLabel.setText("Choose number of players")

        fontBtn = QFont()
        fontBtn.setFamily("Arcade Normal")
        fontBtn.setPointSize(13)

        onePlayerBtn = QPushButton('One Player', self)
        onePlayerBtn.clicked.connect(self.onePlayer)
        onePlayerBtn.resize(200, 50)
        onePlayerBtn.move(310, 400)
        onePlayerBtn.setStyleSheet("QPushButton:!hover { background-color: black; color: white;  }"
                                   "QPushButton:hover {background-color: black; color: red; }")
        onePlayerBtn.setFont(fontBtn)

        twoPlayersBtn = QPushButton('Two Players', self)
        twoPlayersBtn.clicked.connect(self.twoPlayers)
        twoPlayersBtn.resize(200, 50)
        twoPlayersBtn.move(320, 500)
        twoPlayersBtn.setStyleSheet("QPushButton:!hover { background-color: black; color: white; }"
                                    "QPushButton:hover { background-color: black; color: red; }")
        twoPlayersBtn.setFont(fontBtn)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.label = QLabel(self)
        self.label.move(200, 0)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(400, 200, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def onePlayer(self):
        self.board = OnePlayer()
        self.board.show()
        self.close()

    def twoPlayers(self):
        self.board = TwoPlayers()
        self.close()

