from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5.Qt import Qt
import sys
from Tournament import Tournament


class TwoPlayers(QWidget):

    def __init__(self):

        super().__init__()

        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()
        self.setFixedSize(800, 600)

        self.playersName = []
        self.exist = False

        fontTB = QFont()
        fontTB.setFamily("Arcade Normal")
        fontTB.setPointSize(13)

        fontPlayerLabel = QFont()
        fontPlayerLabel.setFamily("Arcade Normal")
        fontPlayerLabel.setPointSize(8)

        fontBtn = QFont()
        fontBtn.setFamily("Arcade Normal")
        fontBtn.setPointSize(13)

        ####################################################################
        self.textLabel = QLabel(self)
        self.textLabel.move(140, 270)
        fontLabel = QFont()
        fontLabel.setFamily("Arcade Normal")
        fontLabel.setPointSize(10)
        self.textLabel.setStyleSheet('color: white;')
        self.textLabel.setFont(fontLabel)
        self.textLabel.setText("Tournament for 4 players. \nEnter player names:")

        '''Player 1'''
        self.playerOneLabel = QLabel(self)
        self.playerOneLabel.move(20, 370)
        self.playerOneLabel.setStyleSheet('color: white;')
        self.playerOneLabel.setFont(fontPlayerLabel)
        self.playerOneLabel.setText("Player 1:")

        self.playerOne = QLineEdit(self)
        self.playerOne.resize(200, 50)
        self.playerOne.move(120, 350)
        self.playerOne.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.playerOne.setFont(fontTB)

        '''Player 2'''
        self.playerTwoLabel = QLabel(self)
        self.playerTwoLabel.move(20, 470)
        self.playerTwoLabel.setStyleSheet('color: white;')
        self.playerTwoLabel.setFont(fontPlayerLabel)
        self.playerTwoLabel.setText("Player 2:")

        self.playerTwo = QLineEdit(self)
        self.playerTwo.resize(200, 50)
        self.playerTwo.move(120, 450)
        self.playerTwo.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.playerTwo.setFont(fontTB)

        '''Player 3'''
        self.playerThreeLabel = QLabel(self)
        self.playerThreeLabel.move(400, 370)
        self.playerThreeLabel.setStyleSheet('color: white;')
        self.playerThreeLabel.setFont(fontPlayerLabel)
        self.playerThreeLabel.setText("Player 3:")

        self.playerThree = QLineEdit(self)
        self.playerThree.resize(200, 50)
        self.playerThree.move(500, 350)
        self.playerThree.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.playerThree.setFont(fontTB)

        '''Player 4 '''
        self.playerFourLabel = QLabel(self)
        self.playerFourLabel.move(400, 470)
        self.playerFourLabel.setStyleSheet('color: white;')
        self.playerFourLabel.setFont(fontPlayerLabel)
        self.playerFourLabel.setText("Player 4:")

        self.playerFour = QLineEdit(self)
        self.playerFour.resize(200, 50)
        self.playerFour.move(500, 450)
        self.playerFour.setStyleSheet("QLineEdit { background-color: black; color: white; }")
        self.playerFour.setFont(fontTB)

        ################################################3
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
        thridPlayer = self.playerThree.text()
        fourthPlayer = self.playerFour.text()
        self.frame = Tournament(fistPlayer, secondPlayer, thridPlayer, fourthPlayer, 1)
        self.close()
