from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtGui import QColor
import sys


class Board(QFrame):
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

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())