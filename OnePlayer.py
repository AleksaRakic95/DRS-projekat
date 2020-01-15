from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5.Qt import Qt
import sys
from Board import Board


class OnePlayer(QWidget):

    def __init__(self):

        super().__init__()

        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()
        self.setFixedSize(800, 600)

        self.textLabel = QLabel(self)
        self.textLabel.move(180, 250)
        fontLabel = QFont()
        fontLabel.setFamily("Arcade Normal")
        fontLabel.setPointSize(20)
        self.textLabel.setStyleSheet('color: white;')
        self.textLabel.setFont(fontLabel)
        self.textLabel.setText("Enter players names")

        fontTB = QFont()
        fontTB.setFamily("Arcade Normal")
        fontTB.setPointSize(13)

        self.player1Label = QLabel(self)
        self.player1Label.move(180, 335)
        self.player1Label.setStyleSheet('color: white;')
        self.player1Label.setFont(fontTB)
        self.player1Label.setText("Player 1: ")

        self.textEdit = QLineEdit(self)
        self.textEdit.resize(200,50)
        self.textEdit.move(340, 320)
        self.textEdit.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.textEdit.setFont(fontTB)

        self.player2Label = QLabel(self)
        self.player2Label.move(180, 425)
        self.player2Label.setStyleSheet('color: white;')
        self.player2Label.setFont(fontTB)
        self.player2Label.setText("Player 2: ")

        self.textEdit2 = QLineEdit(self)
        self.textEdit2.resize(200, 50)
        self.textEdit2.move(340, 410)
        self.textEdit2.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.textEdit2.setFont(fontTB)

        fontBtn = QFont()
        fontBtn.setFamily("Arcade Normal")
        fontBtn.setPointSize(13)

        self.playBtn = QPushButton("Play", self)
        self.playBtn.clicked.connect(self.startGame)
        self.playBtn.resize(200, 50)
        self.playBtn.move(300, 500)
        self.playBtn.setStyleSheet("QPushButton:!hover { background-color: black; color: white;  }"
                                   "QPushButton:hover {background-color: black; color: red; }")
        self.playBtn.setFont(fontBtn)

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

    def startGame(self):
        playernameOne = self.textEdit.text()
        playernameTwo = self.textEdit2.text()
        self.frame = Board(playernameOne, playernameTwo)
        self.close()
