from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QLabel, QFrame, QDesktopWidget

class GameOver(QFrame):
    def __init__(self, winnerName, score):
        super().__init__()

        self.setStyleSheet("QFrame { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()
        self.show()
        self.font = QFont("Arcade Normal", 15, QFont.Bold)

        self.message = QLabel("GAME OVER", self)
        self.message.setFont(self.font)
        self.message.setStyleSheet("color: white")
        self.message.setGeometry(100,130, 250, 60)
        self.message.show()

        self.message1 = QLabel("WINNER IS " + str(winnerName) + " WITH SCORE " + str(score), self)
        self.message1.setFont(self.font)
        self.message1.setStyleSheet("color: white")
        self.message1.setGeometry(100, 300, 700, 60)
        self.message1.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())