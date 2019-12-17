from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(600, 800)

        self.label2 = QLabel(self)
        self.label2.move(350, 400)
        pixmapJump = QPixmap('Assets/Controls/MarioStand.png')
        pixmapCroppedJump = pixmapJump.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap((QPixmap(pixmapCroppedJump)))