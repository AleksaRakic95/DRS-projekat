from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtGui import QColor, QPixmap, QMovie
from PyQt5.QtCore import Qt, QByteArray
import  sys


class Board(QFrame):
    BoardWidth = 200
    BoardHeight = 200

    def __init__(self):
        super().__init__()

        self.initBoard()

    def initBoard(self):
        self.resize(800,600)
        self.center()
        self.setWindowTitle('Donkey Kong')

        self.setStyleSheet("QFrame { background-color: %s}" % QColor(0, 0, 0).name())

        sirina = 800 / 54
        visina = 600 / 40

        brickImage = QPixmap('Assets/Brick/Brick.png')
        brickImageCropped = brickImage.scaled(sirina, visina, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        self.BorderList = []

        for i in range(40):
            for j in range(54):
                if i == 0 or i == 39:
                    self.BorderList.append(self.setBorder(brickImageCropped, i, j, sirina, visina))
                else:
                    if j == 0 or j == 53:
                        self.BorderList.append(self.setBorder(brickImageCropped, i, j, sirina, visina))

        platformImage = QPixmap('Assets/Brick/Platforma.png')
        platformImageCropped = platformImage.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        self.PlatformList = []

        for i in range(1, 6):
            for j in range(36):
                self.PlatformList.append(self.setPlatform(platformImageCropped, i, j, sirina))

        self.setBarrel()

        self.show()

    def setBorder(self, pixmapCropped, i, j, sirina, visina):
        label = QLabel(self)
        label.setPixmap(QPixmap(pixmapCropped))
        label.move(j * sirina, i * visina)
        return label

    def setPlatform(self, platformImageCropped, i, j, sirina):
        label = QLabel(self)
        label.setPixmap(QPixmap(platformImageCropped))

        if i % 2 == 1:
            if i == 5:
                if j > 12 and j < 20:
                    label.move(sirina + j * 20, 600 - i * 90 - 15)
            else:
               label.move(sirina + j * 20, 600 - i * 90 - 15)
        else:
            if i == 4:
                if j > 28:
                    label.move(50 + sirina + j * 20, 600 - i * 90 - 15)
                else:
                    label.move(sirina + j * 20, 600 - i * 90 - 15)
            else:
                label.move(50 + sirina + j * 20, 600 - i * 90 - 15)

        return label

    def setBarrel(self):
        self.barrelLable = QLabel(self)
        barrelImage = QPixmap('Assets/Brick/Barel.png')
        barrelImageCropped = barrelImage.scaled(50, 35, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.barrelLable.setPixmap(QPixmap(barrelImageCropped))
        self.barrelLable.move(25, 550)

        self.movie = QMovie("Assets/Brick/Flame3.gif", QByteArray(), self)
        self.flameLabel = QLabel(self)
        self.flameLabel.move(27, 520)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.flameLabel.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())