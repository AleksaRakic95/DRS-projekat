from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget
from PyQt5.QtGui import QColor, QPixmap, QMovie, QPainter, QFont
from PyQt5.QtCore import Qt, QByteArray
import sys, time, random

from key_notifyer import KeyNotifyer
from MonkeyMovement import MonkeyMovement
from BarrelMovement import BarrelMovement
from PointsCounter import PointsCounter



class Board(QFrame):
    BoardWidth = 200
    BoardHeight = 200
    PocetnaDimenzija = 100

    y = 545
    x = 100

    isJump = 0
    v = 3
    m = 2

    def __init__(self, playerOneName=None, playerTwoName=None):
        self.nameOne = playerOneName
        self.nameTwo = playerTwoName
        super().__init__()

        self.moveRightFlags = 0
        self.moveLeftFlags = 0
        self.moveUpFlags = 0
        self.moveDownFlags = 0
        self.moveRight2Flags = 0
        self.moveLeft2Flags = 0
        self.moveUp2Flags = 0
        self.moveDown2Flags = 0
        self.cekanjePlayer1_1 = 0
        self.cekanjePlayer2_1 = 0
        self.cekanjePlayer1_2 = 0
        self.cekanjePlayer2_2 = 0
        self.movePlayerFlags = 0

        self.hitWall = False
        self.barrels = []

        self.point1 = 0
        self.point2 = 0
        self.first = [True, False, False, False, False, False]
        self.second = [True, False, False, False, False, False]

        self.initBoard()

        self.key_notifyer = KeyNotifyer()
        self.key_notifyer.key_signal.connect(self.__update_position__)
        self.key_notifyer.start()

        self.monkey_movement = MonkeyMovement()
        self.monkey_movement.move_monkey_signal.connect(self.moveMonkey)
        self.monkey_movement.start()

        self.barrel_movement = BarrelMovement()
        self.barrel_movement.move_barrel_signal.connect(self.moveBarrel)
        self.barrel_movement.start()

        self.points_counter = PointsCounter()
        self.points_counter.point_counter_signal.connect(self.refreshPoints)
        self.points_counter.start()

    def initBoard(self):
        self.resize(800,600)
        self.center()
        self.setWindowTitle('Donkey Kong')

        self.setStyleSheet("QFrame { background-color: %s}" % QColor(0, 0, 0).name())

        sirina = 800 / 54                      # sirina kockice za ivicu
        visina = 600 / 40                      #visina kocikice za ivicu

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

        platformRestImage = QPixmap('Assets/Brick/Platforma2.png')
        platformRestCroppedImage = platformRestImage.scaled(10, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        self.PlatformList = []

        for i in range(1, 6):
            for j in range(38):
                self.PlatformList.append(self.setPlatform(platformImageCropped, i, j, sirina))

            self.PlatformList.append(self.setPlatform(platformRestCroppedImage, i, 38, sirina))

        self.setPrincess()
        self.playerName()
        self.setLadder()
        #self.setBarrel()
        self.setAvatars("Assets/Mario/marioR.png", "Assets/Mario/mario2L.png")
        self.setMonkey()

        self.show()

    def playerName(self):
        fontLbl = QFont()
        fontLbl.setFamily("Arcade Normal")
        fontLbl.setPointSize(8)

        self.playerOne = QLabel(self)
        self.playerOne.setText(self.nameOne)
        self.playerOne.setFont(fontLbl)
        self.playerOne.setStyleSheet("QLabel {color: white}")
        self.playerOne.move(20,20)

        self.playerTwo = QLabel(self)
        self.playerTwo.setText(self.nameTwo)
        self.playerTwo.setFont(fontLbl)
        self.playerTwo.setStyleSheet("QLabel {color: white}")
        self.playerTwo.move(720, 20)

    def setBorder(self, pixmapCropped, i, j, sirina, visina):
        label = QLabel(self)
        label.setPixmap(QPixmap(pixmapCropped))
        label.move(j * sirina, i * visina)
        return label

    def setPlatform(self, platformImageCropped, i, j, sirina):
        label = QLabel(self)
        label.setPixmap(QPixmap(platformImageCropped))

        if i < 5:
            label.move(sirina + j * 20, 600 - i * 90 - 15)
        else:
            if j > 12 and j < 20:
                label.move(sirina + j * 20, 600 - i * 90 - 15)
            else:
                label.move(800, 600)

        return label

    def setPrincess(self):
        self.movie = QMovie("Assets/Princess/Princess.gif", QByteArray(), self)
        self.princessLabel = QLabel(self)
        self.princessLabel.setGeometry(285, 95, 80, 40)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.princessLabel.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

    def setLadder(self):
        ladderImage = QPixmap('Assets/Ladder/ladder.png')
        ladderImageCropped = ladderImage.scaled(30, 70, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        ladderImage1 = QPixmap('Assets/Ladder/ladder2.png')
        ladderImage2Cropped = ladderImage1.scaled(30, 70, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        brokenLadderImage = QPixmap('Assets/Ladder/brokenLadder.png')
        brokenLadderImageCropped = brokenLadderImage.scaled(30, 70, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        # Merdevine na prvoj platformi
        self.brokenLadderPosition(brokenLadderImageCropped, 75, 515)
        self.ladderPosition(ladderImageCropped, 350, 515)
        self.ladderPosition(ladderImageCropped, 420, 515)
        self.brokenLadderPosition(brokenLadderImageCropped, 695, 515)

        # Merdevine na drugoj platformi
        self.ladderPosition(ladderImageCropped, 45, 425)
        self.brokenLadderPosition(brokenLadderImageCropped, 320, 425)
        self.brokenLadderPosition(brokenLadderImageCropped, 452, 425)
        self.ladderPosition(ladderImageCropped, 725, 425)

        # Merdevine na trecoj platformi
        self.brokenLadderPosition(brokenLadderImageCropped, 75, 335)
        self.ladderPosition(ladderImageCropped, 350, 335)
        self.ladderPosition(ladderImageCropped, 420, 335)
        self.brokenLadderPosition(brokenLadderImageCropped, 695, 335)

        # Merdevine na cetvrtoj platformi
        self.ladderPosition(ladderImageCropped, 45, 245)
        self.brokenLadderPosition(brokenLadderImageCropped, 320, 245)
        self.brokenLadderPosition(brokenLadderImageCropped, 452, 245)
        self.ladderPosition(ladderImageCropped, 725, 245)

        # Merdevine na petoj platformi
        self.ladderPosition(ladderImageCropped, 382, 155)
        self.ladderPosition(ladderImageCropped, 241, 155)
        self.ladderPosition(ladderImage2Cropped, 241, 85)
        self.ladderPosition(ladderImage2Cropped, 241, 15)
        self.ladderPosition(ladderImageCropped, 191, 155)
        self.ladderPosition(ladderImage2Cropped, 191, 85)
        self.ladderPosition(ladderImage2Cropped, 191, 15)

    def ladderPosition(self, ladderImageCropped, x, y):
        self.ladderlabel = QLabel(self)
        self.ladderlabel.setPixmap(QPixmap(ladderImageCropped))
        self.ladderlabel.move(x, y)  # x=685, y=515

    def brokenLadderPosition(self, brokenLadderImageCropped, x, y):
        self.brokenLadderlabel = QLabel(self)
        self.brokenLadderlabel.setPixmap(QPixmap(brokenLadderImageCropped))
        self.brokenLadderlabel.move(x, y)  # x=350, y=515

    def setAvatars(self, naziv, naziv2):
        ''' Avatar 1 '''

        self.avatarLable = QLabel(self)
        avatarImage = QPixmap(naziv)
        self.avatarLable.setStyleSheet('QLabel { background-color: transparent }')
        avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarLable.setPixmap(QPixmap(avatarImageCropped))
        self.avatarLable.move(40, 545)

        ''' Avatar 2 '''

        self.avatarLable2 = QLabel(self)
        avatarImage2 = QPixmap(naziv2)
        self.avatarLable2.setStyleSheet('QLabel { background-color: transparent }')
        avatarImageCropped2 = avatarImage2.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarLable2.setPixmap(QPixmap(avatarImageCropped2))
        self.avatarLable2.move(720, 545)

    def setMonkey(self):
        self.monkeyLabel = QLabel(self)
        monkeyImage = QPixmap("Assets/Monkey/monkey.png")
        monkeyCroppedImage = monkeyImage.scaled(60, 70, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.monkeyLabel.setStyleSheet('QLabel { background-color: transparent }')
        self.monkeyLabel.setPixmap(QPixmap(monkeyCroppedImage))
        self.monkeyLabel.move(375, 155)

    def moveMonkey(self):
        rect = self.monkeyLabel.geometry()

        if rect.x() == 20:
            self.hitWall = True
        elif rect.x() == 720:
            self.hitWall = False

        rand = random.randint(0, 800)

        if rand % 50 == 0:
            barrel = QLabel(self)
            barrelImage = QPixmap("Assets/Barrel/burrelBrown.png")
            barrelCroppedImage = barrelImage.scaled(28, 18, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            barrel.setStyleSheet('QLabel { background-color: transparent }')
            barrel.setPixmap(QPixmap(barrelCroppedImage))
            barrel.move(rect.x(), rect.y() + 20)
            self.barrels.append(barrel)
            self.barrels[len(self.barrels) - 1].show()

        if self.hitWall:
            self.monkeyLabel.move(rect.x() + 5, rect.y())
        else:
            self.monkeyLabel.move(rect.x() - 5, rect.y())


    def moveBarrel(self):

        for barrel in self.barrels:
            rect = barrel.geometry()
            barrel.move(rect.x(), rect.y() + 4)

    def setAttackBarrel(self):
        self.attackBurrel = QLabel(self)
        attackBurrelImage = QPixmap("Assets/Barrel/burrelBrown.png")
        attackBurrelCroppedImage = attackBurrelImage.scaled(28, 18, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.attackBurrel.setStyleSheet('QLabel { background-color: transparent }')
        self.attackBurrel.setPixmap(QPixmap(attackBurrelCroppedImage))
        self.attackBurrel.move(385, 245)


    def keyPressEvent(self, event):
        self.key_notifyer.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifyer.remove_key(event.key())

    def __update_position__(self, key):
        rect = self.avatarLable.geometry()
        rect2 = self.avatarLable2.geometry()

        if key == Qt.Key_Right:
            if rect.x() < 755:
                if rect.y() == 545 or rect.y() == 455 or rect.y() == 365 or rect.y() == 275 or rect.y() == 185:
                    self.movePlayerFlags = 1
                    self.moveRight()
        elif key == Qt.Key_Left:
            if rect.x() > 20:
                if rect.y() == 545 or rect.y() == 455 or rect.y() == 365 or rect.y() == 275 or rect.y() == 185:
                    self.movePlayerFlags = 1
                    self.moveLeft()
        elif key == Qt.Key_Up:
            if rect.y() <= 545 and rect.y() > 455 or rect.y() <= 365 and rect.y() > 275:
                if rect.x() == 72 or rect.x() == 352 or rect.x() == 424 or rect.x() == 696:
                    self.movePlayerFlags = 1
                    self.moveUp()
            elif rect.y() <= 455 and rect.y() > 365 or rect.y() <= 275 and rect.y() > 185:
                if rect.x() == 48 or rect.x() == 320 or rect.x() == 456 or rect.x() == 728:
                    self.movePlayerFlags = 1
                    self.moveUp()
            elif rect.y() <= 185 and rect.y() > 95:
                if rect.x() == 384:
                    self.movePlayerFlags = 1
                    self.moveUp()
        elif key == Qt.Key_Down:
            if rect.y() < 545 and rect.y() >= 455 or rect.y() < 365 and rect.y() >= 275:
                if rect.x() == 72 or rect.x() == 352 or rect.x() == 424 or rect.x() == 696:
                    self.movePlayerFlags = 1
                    self.moveDown()
            elif rect.y() < 455 and rect.y() >= 365 or rect.y() < 275 and rect.y() >= 185:
                if rect.x() == 48 or rect.x() == 320 or rect.x() == 456 or rect.x() == 728:
                    self.movePlayerFlags = 1
                    self.moveDown()
            elif rect.y() < 185 and rect.y() >= 95:
                if rect.x() == 384:
                    self.movePlayerFlags = 1
                    self.moveDown()
        elif key == Qt.Key_A:
            if rect2.x() > 20:
                if rect2.y() == 545 or rect2.y() == 455 or rect2.y() == 365 or rect2.y() == 275 or rect2.y() == 185:
                    self.movePlayerFlags = 2
                    self.moveLeft()
        elif key == Qt.Key_D:
            if rect2.x() < 755:
                if rect2.y() == 545 or rect2.y() == 455 or rect2.y() == 365 or rect2.y() == 275 or rect2.y() == 185:
                    self.movePlayerFlags = 2
                    self.moveRight()
        elif key == Qt.Key_W:
            if rect2.y() <= 545 and rect2.y() > 455 or rect2.y() <= 365 and rect2.y() > 275:
                if rect2.x() == 72 or rect2.x() == 352 or rect2.x() == 424 or rect2.x() == 696:
                    self.movePlayerFlags = 2
                    self.moveUp()
            elif rect2.y() <= 455 and rect2.y() > 365 or rect2.y() <= 275 and rect2.y() > 185:
                if rect2.x() == 48 or rect2.x() == 320 or rect2.x() == 456 or rect2.x() == 728:
                    self.movePlayerFlags = 2
                    self.moveUp()
            elif rect2.y() <= 185 and rect2.y() > 95:
                if rect2.x() == 384:
                    self.movePlayerFlags = 2
                    self.moveUp()
        elif key == Qt.Key_S:
            if rect2.y() < 545 and rect2.y() >= 455 or rect2.y() < 365 and rect2.y() >= 275:
                if rect2.x() == 72 or rect2.x() == 352 or rect2.x() == 424 or rect2.x() == 696:
                    self.movePlayerFlags = 2
                    self.moveDown()
            elif rect2.y() < 455 and rect2.y() >= 365 or rect2.y() < 275 and rect2.y() >= 185:
                if rect2.x() == 48 or rect2.x() == 320 or rect2.x() == 456 or rect2.x() == 728:
                    self.movePlayerFlags = 2
                    self.moveDown()
            elif rect2.y() < 185 and rect2.y() >= 95:
                if rect2.x() == 384:
                    self.movePlayerFlags = 2
                    self.moveDown()

    def closeEvent(self, event):
        self.key_notifyer.die()

    def moveLeft(self):
        player = self.avatarLable.geometry()
        player2 = self.avatarLable2.geometry()

        if self.movePlayerFlags == 1:
            if self.moveLeftFlags == 0:
                avatarImage = QPixmap("Assets/Mario/marioL1.png")
            elif self.moveLeftFlags == 1:
                avatarImage = QPixmap("Assets/Mario/marioL2.png")

            avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.avatarLable.setPixmap(QPixmap(avatarImageCropped))
            self.avatarLable.move(player.x() - 8, player.y())

            if self.moveLeftFlags == 0:
                self.moveLeftFlags = 1
            else:
                self.moveLeftFlags = 0

        elif self.movePlayerFlags == 2:

            if self.moveLeft2Flags == 0:
                avatarImage = QPixmap("Assets/Mario/mario2L1.png")
            elif self.moveLeft2Flags == 1:
                avatarImage = QPixmap("Assets/Mario/mario2L2.png")

            avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.avatarLable2.setPixmap(QPixmap(avatarImageCropped))
            self.avatarLable2.move(player2.x() - 8, player2.y())

            if self.moveLeft2Flags == 0:
                self.moveLeft2Flags = 1
            else:
                self.moveLeft2Flags = 0

        self.movePlayerFlags = 0

    def moveRight(self):
        player = self.avatarLable.geometry()
        player2 = self.avatarLable2.geometry()

        if self.movePlayerFlags == 1:
            if self.moveRightFlags == 0:
                avatarImage = QPixmap("Assets/Mario/marioR1.png")
            elif self.moveRightFlags == 1:
                avatarImage = QPixmap("Assets/Mario/marioR2.png")

            avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.avatarLable.setPixmap(QPixmap(avatarImageCropped))
            self.avatarLable.move(player.x() + 8, player.y())

            if self.moveRightFlags == 0:
                self.moveRightFlags = 1
            else:
                self.moveRightFlags = 0

        elif self.movePlayerFlags == 2:

            if self.moveRight2Flags == 0:
                avatarImage = QPixmap("Assets/Mario/mario2R1.png")
            elif self.moveRight2Flags == 1:
                avatarImage = QPixmap("Assets/Mario/mario2R2.png")

            avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.avatarLable2.setPixmap(QPixmap(avatarImageCropped))
            self.avatarLable2.move(player2.x() + 8, player2.y())

            if self.moveRight2Flags == 0:
                self.moveRight2Flags = 1
            else:
                self.moveRight2Flags = 0

        self.movePlayerFlags = 0

    def moveUp(self):
        if self.movePlayerFlags == 1:
            self.cekanjePlayer1_1 = self.cekanjePlayer1_1 + 1

            if self.cekanjePlayer1_1 % 2 == 0:
                if self.moveUpFlags == 0:
                    avatarImage = QPixmap("Assets/Mario/marioUp1.png")
                elif self.moveUpFlags == 1:
                    avatarImage = QPixmap("Assets/Mario/marioUp11.png")

                if self.moveUpFlags == 0:
                    self.moveUpFlags = 1
                else:
                    self.moveUpFlags = 0

                avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.avatarLable.setPixmap(QPixmap(avatarImageCropped))

            nivo = self.avatarLable.geometry().y()
            x = self.avatarLable.geometry().x()

            if self.OnLadderOrBrokenLadder(nivo, x, 'Up'):
                self.avatarLable.move(x, nivo - 3)

        elif self.movePlayerFlags == 2:
            self.cekanjePlayer2_1 = self.cekanjePlayer2_1 + 1

            if self.cekanjePlayer2_1 % 2 == 0:
                if self.moveUp2Flags == 0:
                    avatarImage = QPixmap("Assets/Mario/mario2Up1.png")
                elif self.moveUp2Flags == 1:
                    avatarImage = QPixmap("Assets/Mario/mario2Up2.png")

                if self.moveUp2Flags == 0:
                    self.moveUp2Flags = 1
                else:
                    self.moveUp2Flags = 0

                avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.avatarLable2.setPixmap(QPixmap(avatarImageCropped))

            nivo = self.avatarLable2.geometry().y()
            x = self.avatarLable2.geometry().x()

            if self.OnLadderOrBrokenLadder(nivo, x, 'Up'):
                self.avatarLable2.move(x, nivo - 3)

        self.movePlayerFlags = 0

    def moveDown(self):

        if self.movePlayerFlags == 1:
            self.cekanjePlayer1_2 = self.cekanjePlayer1_2 + 1

            if self.cekanjePlayer1_2 % 2 == 0:
                if self.moveDownFlags == 0:
                    avatarImage = QPixmap("Assets/Mario/marioUp1.png")
                elif self.moveDownFlags == 1:
                    avatarImage = QPixmap("Assets/Mario/marioUp11.png")

                if self.moveDownFlags == 0:
                    self.moveDownFlags = 1
                else:
                    self.moveDownFlags = 0

                avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.avatarLable.setPixmap(QPixmap(avatarImageCropped))

            nivo = self.avatarLable.geometry().y()
            x = self.avatarLable.geometry().x()

            if self.OnLadderOrBrokenLadder(nivo, x, 'Down'):
                self.avatarLable.move(x, nivo + 3)

        elif self.movePlayerFlags == 2:
            self.cekanjePlayer2_2 = self.cekanjePlayer2_2 + 1

            if self.cekanjePlayer2_2 % 2 == 0:
                if self.moveDown2Flags == 0:
                    avatarImage = QPixmap("Assets/Mario/mario2Up1.png")
                elif self.moveDown2Flags == 1:
                    avatarImage = QPixmap("Assets/Mario/mario2Up2.png")

                if self.moveDown2Flags == 0:
                    self.moveDown2Flags = 1
                else:
                    self.moveDown2Flags = 0

                avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.avatarLable2.setPixmap(QPixmap(avatarImageCropped))

            nivo = self.avatarLable2.geometry().y()
            x = self.avatarLable2.geometry().x()

            if self.OnLadderOrBrokenLadder(nivo, x, 'Down'):
                self.avatarLable2.move(x, nivo + 3)

        self.movePlayerFlags = 0

    def OnLadderOrBrokenLadder(self, nivo, x, direction):
        dodatak = 0
        if direction == 'Up':
            dodatak = 2

        if nivo <= 543 + dodatak and nivo >= 455 + dodatak:
            if x == 352 or x == 424:
                return True
        elif nivo <= 453 + dodatak and nivo >= 365 + dodatak:
            if x == 48 or x == 728:
                return True
        elif nivo <= 363 + dodatak and nivo >= 275 + dodatak:
            if x == 352 or x == 424:
                return True
        elif nivo <= 273 + dodatak and nivo >= 185 + dodatak:
            if x == 48 or x == 728:
                return True
        elif nivo <= 183 + dodatak and nivo >= 95 + dodatak:
            if x == 384:
                return True

        ''' Move down on broken Ladder '''

        if nivo <= 543 + dodatak and nivo >= 521 + dodatak:
            if x == 72 or x == 696:
                return True
        elif nivo <= 453 + dodatak and nivo >= 431 + dodatak:
            if x == 320 or x == 456:
                return True
        elif nivo <= 363 + dodatak and nivo >= 341 + dodatak:
            if x == 72 or x == 696:
                return True
        elif nivo <= 273 + dodatak and nivo >= 249 + dodatak:
            if x == 320 or x == 456:
                return True

        return False

    def refreshPoints(self):
        position1 = self.avatarLable.geometry().y()
        position2 = self.avatarLable2.geometry().y()

        if position1 == 545:
            self.first[0] = True
        elif position1 == 455:
            self.first[0] = False
            self.first[1] = True
        elif position1 == 365:
            self.first[1] = False
            self.first[2] = True
        elif position1 == 275:
            self.first[2] = False
            self.first[3] = True
        elif position1 == 185:
            self.first[3] = False
            self.first[4] = True
        elif position1 == 95:
            self.first[4] = False
            self.first[5] = True
        else:
            self.first[5] = False

        if self.first[0] == True:
            self.point1 = 0
            self.first[0] = False
        elif self.first[1] == True:
            self.point1 = 1
            self.first[1] = False
        elif self.first[2] == True:
            self.point1 = 2
            self.first[2] = False
        elif self.first[3] == True:
            self.point1 = 3
            self.first[3] = False
        elif self.first[4] == True:
            self.point1 = 4
            self.first[4] = False
        elif self.first[5] == True:
            self.point1 = 5
            self.first[5] = False
        else:
            self.point1 = self.point1

        if position2 == 545:
            self.second[0] = True
        elif position2 == 455:
            self.second[0] = False
            self.second[1] = True
        elif position2 == 365:
            self.second[1] = False
            self.second[2] = True
        elif position2 == 275:
            self.second[2] = False
            self.second[3] = True
        elif position2 == 185:
            self.second[3] = False
            self.second[4] = True
        elif position2 == 95:
            self.second[4] = False
            self.second[5] = True
        else:
            self.second[5] = False

        if self.second[0] == True:
            self.point2 = 0
            self.second[0] = False
        elif self.second[1] == True:
            self.point2 = 1
            self.second[1] = False
        elif self.second[2] == True:
            self.point2 = 2
            self.second[2] = False
        elif self.second[3] == True:
            self.point2 = 3
            self.second[3] = False
        elif self.second[4] == True:
            self.point2 = 4
            self.second[4] = False
        elif self.second[5] == True:
            self.point2 = 5
            self.second[5] = False
        else:
            self.point2 = self.point2

        print("point1: " + str(self.point1))
        print("point2: " + str(self.point2))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class BoardTwoPlayers(QFrame):
    startingPositionOne = 100
    startingPositionTwo = 500

    def __init__(self, playerOneName=None, playerTwoName=None):
        self.pOneName = playerOneName
        self.pTwoName = playerTwoName

        super().__init__()

        self.initBoardTwoPlayers()

        self.key_notifyer = KeyNotifyer()
        self.key_notifyer.key_signal.connect(self.__update_position__)
        self.key_notifyer.start()

    def initBoardTwoPlayers(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle("Donkey Kong")

        self.setStyleSheet("QFrame {background-color: black;} ")

        width = 800 / 54
        height = 600 / 40

        brickImage = QPixmap('Assets/Brick/Brick.png')
        brickImageCropped = brickImage.scaled(width, height, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        self.BorderList = []

        for i in range(40):
            for j in range(54):
                if i == 0 or i == 39:
                    self.BorderList.append(self.setBorder(brickImageCropped, i, j, width, height))
                else:
                    if j == 0 or j == 53:
                        self.BorderList.append(self.setBorder(brickImageCropped, i, j, width, height))

        platformImage = QPixmap('Assets/Brick/Platforma.png')
        platformImageCropped = platformImage.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        self.PlatformList = []

        for i in range(1, 6):
            for j in range(36):
                self.PlatformList.append(self.setPlatform(platformImageCropped, i, j, width))

        self.playerNames()
        self.setBarrel()
        self.setAvatars("Assets/Mario/marioR.png", "Assets/Mario/marioL.png")

        self.show()

    def playerNames(self):
        self.player1 = QLabel(self)
        self.player2 = QLabel(self)

        fontLbl = QFont()
        fontLbl.setFamily("Arcade Normal")
        fontLbl.setPointSize(8)

        self.player1.setText(self.pOneName)
        self.player1.setFont(fontLbl)
        self.player1.setStyleSheet("QLabel {color: white;} ")
        self.player1.move(20, 20)

        self.player2.setText(self.pTwoName)
        self.player2.setFont(fontLbl)
        self.player2.setStyleSheet("QLabel {color: white;} ")
        self.player2.move(700, 20)

    def setBorder(self, pixmapCropped, i, j, width, height):
        label = QLabel(self)
        label.setPixmap(QPixmap(pixmapCropped))
        label.move(j * width, i * height)
        return label

    def setPlatform(self, pixmapCropped, i, j, width):
        label = QLabel(self)
        label.setPixmap(QPixmap(pixmapCropped))

        if i % 2 == 1:
            if i == 5:
                if j > 12 and j < 20:
                    label.move(width + j * 20, 600 - i * 90 - 15)
            else:
                label.move(width + j * 20, 600 - i * 90 - 15)
        else:
            if i == 4:
                if j > 28:
                    label.move(50 + width + j * 20, 600 - i * 90 - 15)
                else:
                    label.move(width + j * 20, 600 - i * 90 - 15)
            else:
                label.move(50 + width + j * 20, 600 - i * 90 - 15)

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

    def setAvatars(self, avatarOne, avatarTwo):
        self.avatarOneLbl = QLabel(self)
        avatarImageOne = QPixmap(avatarOne)
        self.avatarOneLbl.setStyleSheet('QLabel { background-color: transparent }')
        #avatarImageOne.fill(Qt.transparent)
        avatarImageOneCropped = avatarImageOne.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarOneLbl.setPixmap(QPixmap(avatarImageOneCropped))
        self.avatarOneLbl.move(100, 545)

        self.avatarTwoLbl = QLabel(self)
        avatarImageTwo = QPixmap(avatarTwo)
        self.avatarTwoLbl.setStyleSheet('QLabel { background-color: transparent }')
        #avatarImageTwo.fill(Qt.transparent)
        avatarImageTwoCropped = avatarImageTwo.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarTwoLbl.setPixmap(QPixmap(avatarImageTwoCropped))
        self.avatarTwoLbl.move(500, 545)

    def setAvatarOneMove(self, avatar):
        avatarImage = QPixmap(avatar)
        avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarOneLbl.setPixmap(QPixmap(avatarImageCropped))

    def setAvatarTwoMove(self, avatar):
        avatarImage = QPixmap(avatar)
        avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarTwoLbl.setPixmap(QPixmap(avatarImageCropped))

    def keyPressEvent(self, event):
        self.key_notifyer.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifyer.remove_key(event.key())

    def __update_position__(self, key):
        player1 = self.avatarOneLbl.geometry()
        player2 = self.avatarTwoLbl.geometry()

        ''' Moving first player '''

        if key == Qt.Key_Right:
            if player1.x() < 755:
                self.avatarOneLbl.setGeometry(player1.x() + 5, player1.y(), player1.width(), player1.height())
        elif key == Qt.Key_Left:
            if player1.x() > 81:
                self.avatarOneLbl.setGeometry(player1.x() - 5, player1.y(), player1.width(), player1.height())

        ''' Moving second player '''

        if key == Qt.Key_D:
            if player2.x() < 755:
                self.avatarTwoLbl.setGeometry(player2.x() + 5, player2.y(), player2.width(), player2.height())
        elif key == Qt.Key_A:
            if player2.x() > 81:
                self.avatarTwoLbl.setGeometry(player2.x() - 5, player2.y(), player2.width(), player2.height())

    def closeEvent(self, event):
        self.key_notifyer.die()



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
