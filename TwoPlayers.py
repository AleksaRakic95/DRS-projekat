from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5.Qt import Qt
import sys
from Board import BoardTwoPlayers


class TwoPlayers(QWidget):

    def __init__(self):

        super().__init__()

        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()
        self.setFixedSize(800, 600)

        self.textLabel = QLabel(self)
        self.textLabel.move(140, 270)
        fontLabel = QFont()
        fontLabel.setFamily("Arcade Normal")
        fontLabel.setPointSize(20)
        self.textLabel.setStyleSheet('color: white;')
        self.textLabel.setFont(fontLabel)
        self.textLabel.setText("Enter player names")

        self.playerOneLabel = QLabel(self)
        self.playerOneLabel.move(150, 370)
        fontPlayerLabel = QFont()
        fontPlayerLabel.setFamily("Arcade Normal")
        fontPlayerLabel.setPointSize(13)
        self.playerOneLabel.setStyleSheet('color: white;')
        self.playerOneLabel.setFont(fontPlayerLabel)
        self.playerOneLabel.setText("Player one ")

        fontTB = QFont()
        fontTB.setFamily("Arcade Normal")
        fontTB.setPointSize(13)

        self.playerOne = QLineEdit(self)
        self.playerOne.resize(200, 50)
        self.playerOne.move(350, 350)
        self.playerOne.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.playerOne.setFont(fontTB)

        fontBtn = QFont()
        fontBtn.setFamily("Arcade Normal")
        fontBtn.setPointSize(13)

        self.playerTwoLabel = QLabel(self)
        self.playerTwoLabel.move(150, 470)
        self.playerTwoLabel.setStyleSheet('color: white;')
        self.playerTwoLabel.setFont(fontPlayerLabel)
        self.playerTwoLabel.setText("Player two ")

        self.playerTwo = QLineEdit(self)
        self.playerTwo.resize(200, 50)
        self.playerTwo.move(350, 450)
        self.playerTwo.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.playerTwo.setFont(fontTB)

        self.playBtn = QPushButton("Play", self)
        self.playBtn.clicked.connect(self.startGame)
        self.playBtn.resize(200, 50)
        self.playBtn.move(250, 525)
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
        fistPlayer = self.playerOne.text()
        secondPlayer = self.playerTwo.text()
        self.frame = BoardTwoPlayers(fistPlayer, secondPlayer)
        self.close()
