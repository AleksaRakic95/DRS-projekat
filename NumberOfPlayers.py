from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QColor, QFont
import sys


class NumberOfPlayers(QFrame):
    BoardWidth = 200
    BoardHeight = 200

    def __init__(self):
        super().__init__()

        self.initBoard()

    def initBoard(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Donkey Kong')

        self.setStyleSheet("QFrame { background-color: %s}" % QColor(0, 0, 0).name())

        self.textLabel = QLabel(self)
        self.textLabel.move(30, 200)
        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(13)
        self.textLabel.setStyleSheet('color: white;')
        self.textLabel.setFont(font)
        self.textLabel.setText("Choose how the number of players")

        onePlayerButton = QPushButton('One Player', self)
        onePlayerButton.clicked.connect(self.OnePlayer)
        onePlayerButton.resize(130, 50)
        onePlayerButton.move(340, 400)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())