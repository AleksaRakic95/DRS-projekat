from PyQt5.QtWidgets import  QWidget, QPushButton, QFrame, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5.Qt import Qt, QElapsedTimer
import time

class Controls(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()

        self.label = QLabel(self)
        self.label.move(200,0)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(400, 200, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.labelText = QLabel(self)
        self.labelText.move(30, 250)
        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(13)
        self.labelText.setStyleSheet('color: white;')
        self.labelText.setFont(font)
        self.labelText.setText("Press the arrow keys to move left and right")

        self.label2 = QLabel(self)
        self.label2.move(290, 300)
        pixmapLeft = QPixmap('Assets/Controls/levo.png')
        pixmapCroppedLeft = pixmapLeft.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap((QPixmap(pixmapCroppedLeft)))

        self.label3 = QLabel(self)
        self.label3.move(450, 300)
        pixmapRight = QPixmap('Assets/Controls/desno.png')
        pixmapCroppedRight = pixmapRight.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label3.setPixmap((QPixmap(pixmapCroppedRight)))

        self.label4 = QLabel(self)
        self.label4.move(290, 400)
        pixmapMarioLeft = QPixmap('Assets/Controls/leviMario.png')
        pixmapCroppedMarioLeft = pixmapMarioLeft.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label4.setPixmap((QPixmap(pixmapCroppedMarioLeft)))

        self.label5 = QLabel(self)
        self.label5.move(450, 400)
        pixmapMarioRight = QPixmap('Assets/Controls/desniMario.png')
        pixmapCroppedMarioRight = pixmapMarioRight.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label5.setPixmap((QPixmap(pixmapCroppedMarioRight)))

        self.labelText2 = QLabel(self)
        self.labelText2.move(240, 500)
        self.labelText2.setStyleSheet('color: white;')
        self.labelText2.setFont(font)
        self.labelText2.setText("Press N to continue")

        self.show()
        #self.close()
        #frame = ControlsJump()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_N:
            self.close()
            self.frame = ControlsJump()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())


class ControlsJump(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()

        self.label = QLabel(self)
        self.label.move(200, 0)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(400, 200, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.labelText = QLabel(self)
        self.labelText.move(230, 250)
        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(13)
        self.labelText.setStyleSheet('color: white;')
        self.labelText.setFont(font)
        self.labelText.setText("Press Space to jump")

        self.label1 = QLabel(self)
        self.label1.move(240, 300)
        pixmapSpace = QPixmap('Assets/Controls/jump.png')
        pixmapCroppedSpace = pixmapSpace.scaled(300, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap((QPixmap(pixmapCroppedSpace)))

        self.label2 = QLabel(self)
        self.label2.move(350, 400)
        pixmapJump = QPixmap('Assets/Controls/MarioStand.png')
        pixmapCroppedJump = pixmapJump.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap((QPixmap(pixmapCroppedJump)))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)