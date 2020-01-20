from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QLabel, QFrame, QDesktopWidget, QPushButton

class GameOver(QFrame):
    def __init__(self, winnerName, score):
        super().__init__()

        self.setStyleSheet("QFrame { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()

        self.show()

        self.font = QFont("Arcade Normal", 15, QFont.Bold)

        self.message = QLabel("GAME OVER", self)
        self.message.setFont(QFont('Arcade Normal', 60, QFont.Bold))
        self.message.setStyleSheet("color: white")
        self.message.setGeometry(50, 50, 700, 100)
        self.message.show()

        self.message1 = QLabel("WINNER IS " + str(winnerName) + " WITH SCORE " + str(score), self)
        self.message1.setFont(self.font)
        self.message1.setStyleSheet("color: white")
        self.message1.setGeometry(70, 200, 700, 60)
        self.message1.show()

        fontBtn = QFont()
        fontBtn.setFamily("Arcade Normal")
        fontBtn.setPointSize(13)

        self.ExitBtn = QPushButton("Exit", self)
        self.ExitBtn.clicked.connect(self.closeApp)
        self.ExitBtn.resize(100, 50)
        self.ExitBtn.move(350, 400)
        self.ExitBtn.setStyleSheet("QPushButton:!hover { background-color: black; color: white;  }"
                                   "QPushButton:hover {background-color: black; color: red; }")
        self.ExitBtn.setFont(fontBtn)
        self.ExitBtn.show()

    def closeApp(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())