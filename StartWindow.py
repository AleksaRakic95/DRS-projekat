from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon, QPixmap, QImage, QFont
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from Board import Board
from NumberOfPlayers import NumberOfPlayers
import sys


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Donkey Kong'

        self.setStyleSheet("QWidget { background-color: %s}" % QColor(0, 0, 0).name())
        self.resize(800, 600)
        self.center()

        pybutton1 = QPushButton('New Game', self)
        pybutton1.clicked.connect(self.clickMethod1)
        pybutton1.resize(180, 50)
        pybutton1.move(310, 400)

        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(15)
        font.bold()

        pybutton1.setStyleSheet("QPushButton:!hover { background-color: black; color: white; }"
                                "QPushButton:hover { background-color: black; color: red; }")
        pybutton1.setFont(font)

        pybutton2 = QPushButton('Controls', self)
        pybutton2.clicked.connect(self.clickMethod2)
        pybutton2.resize(160, 50)
        pybutton2.move(320, 500)

        pybutton2.setStyleSheet("QPushButton:!hover { background-color: black; color: white; }"
                                "QPushButton:hover { background-color: black; color: red; }")
        pybutton2.setFont(font)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.label = QLabel(self)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(800, 300, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def clickMethod1(self):
        self.board = NumberOfPlayers()
        self.close()

    def clickMethod2(self):
        self.frame = Controls()
        self.close()

class Controls(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("QWidget { background-color: %s}" % QColor(-1, 0, 0).name())
        self.resize(799, 600)
        self.center()

        self.label = QLabel(self)
        self.label.move(199,0)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(399, 200, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.labelText = QLabel(self)
        self.labelText.move(10, 250)
        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(12)
        self.labelText.setStyleSheet('color: white;')
        self.labelText.setFont(font)
        self.labelText.setText("Press the arrow keys to move left and right\nPress the up arrow key to move up the ladders\nPress the down arrow key to move down the ladders")

        self.label1 = QLabel(self)
        self.label1.move(150, 320)
        pixmapLeft = QPixmap('Assets/Controls/levo.png')
        pixmapCroppedLeft = pixmapLeft.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap((QPixmap(pixmapCroppedLeft)))

        self.label2 = QLabel(self)
        self.label2.move(300, 320)
        pixmapRight = QPixmap('Assets/Controls/desno.png')
        pixmapCroppedRight = pixmapRight.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap((QPixmap(pixmapCroppedRight)))

        self.labelup = QLabel(self)
        self.labelup.move(450, 320)
        pixmapup = QPixmap('Assets/Controls/gore.png')
        pixmapCroppedup = pixmapup.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labelup.setPixmap((QPixmap(pixmapCroppedup)))

        self.labeldown = QLabel(self)
        self.labeldown.move(600, 320)
        pixmapdown = QPixmap('Assets/Controls/dole.png')
        pixmapCroppeddown = pixmapdown.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labeldown.setPixmap((QPixmap(pixmapCroppeddown)))

        self.label3 = QLabel(self)
        self.label3.move(150, 400)
        pixmapMarioLeft = QPixmap('Assets/Controls/leviMario.png')
        pixmapCroppedMarioLeft = pixmapMarioLeft.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label3.setPixmap((QPixmap(pixmapCroppedMarioLeft)))

        self.label4 = QLabel(self)
        self.label4.move(300, 400)
        pixmapMarioRight = QPixmap('Assets/Controls/desniMario.png')
        pixmapCroppedMarioRight = pixmapMarioRight.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label4.setPixmap((QPixmap(pixmapCroppedMarioRight)))

        self.labelUM = QLabel(self)
        self.labelUM.move(450, 400)
        pixmapMarioUp = QPixmap('Assets/Mario/marioUp11.png')
        pixmapCroppedMarioUp = pixmapMarioUp.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labelUM.setPixmap((QPixmap(pixmapCroppedMarioUp)))

        self.labelDM = QLabel(self)
        self.labelDM.move(600, 400)
        pixmapMarioDown = QPixmap('Assets/Mario/marioUp1.png')
        pixmapCroppedMarioDown = pixmapMarioDown.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labelDM.setPixmap((QPixmap(pixmapCroppedMarioDown)))

        self.labelText1 = QLabel(self)
        self.labelText1.move(240, 500)
        self.labelText1.setStyleSheet('color: white;')
        self.labelText1.setFont(font)
        self.labelText1.setText("Press N to continue")

        self.show()
        #self.close()
        #frame = ControlsJump()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_N:
            self.close()
            self.frame = PlayerTwoControls()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())


class PlayerTwoControls(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("QWidget { background-color: %s}" % QColor(-1, 0, 0).name())
        self.resize(799, 600)
        self.center()

        self.label = QLabel(self)
        self.label.move(199, 0)
        pixmapFull = QPixmap('Assets/DonkeyKongLogo.jpg')
        pixmapCropped = pixmapFull.scaled(399, 200, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label.setPixmap((QPixmap(pixmapCropped)))

        self.labelText = QLabel(self)
        self.labelText.move(29, 250)
        font = QFont()
        font.setFamily("Arcade Normal")
        font.setPointSize(12)
        self.labelText.setStyleSheet('color: white;')
        self.labelText.setFont(font)
        self.labelText.setText(
            "Press A or D keys to move left and right\nPress W key to move up the ladders\nPress S key to move down the ladders")

        self.label1 = QLabel(self)
        self.label1.move(150, 320)
        pixmapLeft = QPixmap('Assets/Controls/A.png')
        pixmapCroppedLeft = pixmapLeft.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap((QPixmap(pixmapCroppedLeft)))

        self.label2 = QLabel(self)
        self.label2.move(300, 320)
        pixmapRight = QPixmap('Assets/Controls/D.png')
        pixmapCroppedRight = pixmapRight.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap((QPixmap(pixmapCroppedRight)))

        self.labelup = QLabel(self)
        self.labelup.move(450, 320)
        pixmapup = QPixmap('Assets/Controls/W.png')
        pixmapCroppedup = pixmapup.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labelup.setPixmap((QPixmap(pixmapCroppedup)))

        self.labeldown = QLabel(self)
        self.labeldown.move(600, 320)
        pixmapdown = QPixmap('Assets/Controls/S.png')
        pixmapCroppeddown = pixmapdown.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labeldown.setPixmap((QPixmap(pixmapCroppeddown)))

        self.label3 = QLabel(self)
        self.label3.move(150, 400)
        pixmapMarioLeft = QPixmap('Assets/Mario/mario2L1.png')
        pixmapCroppedMarioLeft = pixmapMarioLeft.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label3.setPixmap((QPixmap(pixmapCroppedMarioLeft)))

        self.label4 = QLabel(self)
        self.label4.move(300, 400)
        pixmapMarioRight = QPixmap('Assets/Mario/mario2R1.png')
        pixmapCroppedMarioRight = pixmapMarioRight.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label4.setPixmap((QPixmap(pixmapCroppedMarioRight)))

        self.labelUM = QLabel(self)
        self.labelUM.move(450, 400)
        pixmapMarioUp = QPixmap('Assets/Mario/mario2Up2.png')
        pixmapCroppedMarioUp = pixmapMarioUp.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labelUM.setPixmap((QPixmap(pixmapCroppedMarioUp)))

        self.labelDM = QLabel(self)
        self.labelDM.move(600, 400)
        pixmapMarioDown = QPixmap('Assets/Mario/mario2Up1.png')
        pixmapCroppedMarioDown = pixmapMarioDown.scaled(59, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.labelDM.setPixmap((QPixmap(pixmapCroppedMarioDown)))

        self.labelText1 = QLabel(self)
        self.labelText1.move(240, 500)
        self.labelText1.setStyleSheet('color: white;')
        self.labelText1.setFont(font)
        self.labelText1.setText("Press N to continue")

        self.show()
        # self.close()
        # frame = ControlsJump()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_N:
            self.close()
            self.frame = StartWindow()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

