from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget
from PyQt5.QtGui import QColor, QPixmap, QMovie, QPainter, QFont, QTextBlock
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal
import sys, time, random

from key_notifyer import KeyNotifyer
from MonkeyMovement import MonkeyMovement
from BarrelMovement import BarrelMovement
from PointsCounter import PointsCounter
from UnexpectedForceLife import UnexpectedForceLife
from UnexpectedForceBomb import UnexpectedForceBomb
from UnexpectedForce import UnexpectedForce
from DelayedEffectOfForce import DelayedEffectOfForce
from GameOver import GameOver


class Board(QFrame):
    BoardWidth = 200
    BoardHeight = 200
    PocetnaDimenzija = 100

    y = 545
    x = 100

    isJump = 0
    v = 3
    m = 2

    def __init__(self, playerOneName=None, playerTwoName=None, level=None):
        self.nameOne = playerOneName
        self.nameTwo = playerTwoName
        self.level = level

        super().__init__()

        self.PlatformChanged = 0

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

        self.avatar1hitHeart = False
        self.avatar2hitHeart = False
        self.avatar1hitBomb = False
        self.avatar2hitBomb = False

        self.bombExist = False
        self.LifeExist = False

        self.hitWall = False
        self.barrels = []

        self.Lives1 = 3
        self.Lives2 = 3

        self.isLive1 = True
        self.isLive2 = True

        self.point1 = 0
        self.point2 = 0
        self.first = [True, False, False, False, False, False]
        self.second = [True, False, False, False, False, False]

        self.pamtiPrvog = 0
        self.pamtiDrugog = 0

        self.pobednik = 0

        self.initBoard()

        self.key_notifyer = KeyNotifyer()
        self.key_notifyer.key_signal.connect(self.__update_position__)
        self.key_notifyer.start()

        self.monkey_movement = MonkeyMovement(self.level)
        self.monkey_movement.move_monkey_signal.connect(self.moveMonkey)
        self.monkey_movement.start(1)

        self.barrel_movement = BarrelMovement(self.level)
        self.barrel_movement.move_barrel_signal.connect(self.moveBarrel)
        self.barrel_movement.start(1)

        self.points_counter = PointsCounter()
        self.points_counter.point_counter_signal.connect(self.refreshPoints)
        self.points_counter.start()

        self.unexpected_force_life = UnexpectedForceLife(self)
        self.unexpected_force_life.show_life_signal.connect(self.showLifeForce)
        self.unexpected_force_life.hide_life_signal.connect(self.hideLifeForce)
        self.unexpected_force_life.start()

        self.unexpected_force_bomb = UnexpectedForceBomb(self)
        self.unexpected_force_bomb.show_bomb_signal.connect(self.showBombForce)
        self.unexpected_force_bomb.hide_bomb_signal.connect(self.hideBombForce)
        self.unexpected_force_bomb.start()

        self.unexpected_force = UnexpectedForce()
        self.unexpected_force.mario1_signal.connect(self.executeForce)
        self.unexpected_force.mario2_signal.connect(self.executeForce2)
        self.unexpected_force.start()

        self.delayed_effect_of_force = DelayedEffectOfForce()
        self.delayed_effect_of_force.delayed_effect_of_force_signal.connect(self.checkCollisionWithUnexpectedForce)
        self.delayed_effect_of_force.start()

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

        if self.nameOne == "":
            self.nameOne = 'Player 1'

        if self.nameTwo == "":
            self.nameTwo = 'Player 2'

        self.levelLabel = QLabel(self)
        self.levelLabel.setText('Level ' + str(self.level))
        self.levelLabel.setFont(fontLbl)
        self.levelLabel.setStyleSheet("QLabel {color: white}")
        self.levelLabel.move(20, 20)

        self.playerOne = QLabel(self)
        self.playerOne.setText(self.nameOne)
        self.playerOne.setFont(fontLbl)
        self.playerOne.setStyleSheet("QLabel {color: red}")
        self.playerOne.move(400,20)

        self.player1score = QLabel(self)
        self.player1score.setText('Score: ')
        self.player1score.setFont(fontLbl)
        self.player1score.setStyleSheet("QLabel {color: red}")
        #self.player1score.move(400, 40)
        self.player1score.setGeometry(400, 35, 100, 20)

        self.player1lives = QLabel(self)
        self.player1lives.setText('Lives: ' + str(self.Lives1))
        self.player1lives.setFont(fontLbl)
        self.player1lives.setStyleSheet("QLabel {color: red}")
        self.player1lives.move(400, 60)

        self.playerTwo = QLabel(self)
        self.playerTwo.setText(self.nameTwo)
        self.playerTwo.setFont(fontLbl)
        self.playerTwo.setStyleSheet("QLabel {color: green}")
        self.playerTwo.move(640, 20)

        self.player2score = QLabel(self)
        self.player2score.setText('Score: ')
        self.player2score.setFont(fontLbl)
        self.player2score.setStyleSheet("QLabel {color: green}")
        self.player2score.setGeometry(640, 35, 100, 20)
        #self.player2score.move(640, 40)

        self.player2lives = QLabel(self)
        self.player2lives.setText('Lives: ' + str(self.Lives1))
        self.player2lives.setFont(fontLbl)
        self.player2lives.setStyleSheet("QLabel {color: green}")
        self.player2lives.move(640, 60)

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

        label.show()

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

        self.manjiRand = random.randrange(20,375)
        self.veciRand = random.randrange(self.manjiRand, 720)

    def moveMonkey(self):
        rect = self.monkeyLabel.geometry()

        rand = random.randrange(self.manjiRand, self.veciRand)

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
            if rect.x() >= self.veciRand:
                self.hitWall = False
                self.manjiRand = random.randrange(0, self.veciRand)
            else:
                self.monkeyLabel.move(rect.x() + 5, rect.y())
        else:
            if rect.x() <= self.manjiRand:
                self.hitWall = True
                self.veciRand = random.randrange(self.manjiRand, 720)
            else:
                self.monkeyLabel.move(rect.x() - 5, rect.y())

        if self.isHit(self.monkeyLabel, self.avatarLable) and self.isLive1:
            print('Sudaaar')
            self.Lives1 = self.Lives1 - 1
            self.player1lives.setText('Lives: ' + str(self.Lives1))
            if (self.Lives1 > 0):
                self.avatarLable.move(40, 545)
            else:
                self.isLive1 = False
                self.avatarLable.clear()
                self.avatarLable.move(1000, 1000)
        elif self.isHit(self.monkeyLabel, self.avatarLable2) and self.isLive2:
            print('Sudaaar')
            self.Lives2 = self.Lives2 - 1
            self.player2lives.setText('Lives: ' + str(self.Lives2))
            if (self.Lives2 > 0):
                self.avatarLable2.move(720, 545)
            else:
                self.isLive2 = False
                self.avatarLable2.clear()
                self.avatarLable2.move(1100, 1100)
        self.isGameOver()

    def moveBarrel(self):

        for barrel in self.barrels:
            rect = barrel.geometry()
            barrel.move(rect.x(), rect.y() + 4)

            if self.isHit(barrel, self.avatarLable) and self.isLive1:
                print('Sudaaar')
                self.Lives1 = self.Lives1 - 1
                self.player1lives.setText('Lives: ' + str(self.Lives1))
                #barrel.move(0,0)
                barrel.hide()
                self.barrels.remove(barrel)
                if(self.Lives1 > 0):
                    self.avatarLable.move(40, 545)
                else:
                    self.isLive1 = False
                    self.avatarLable.clear()
                    self.avatarLable.move(1000, 1000)
            elif self.isHit(barrel, self.avatarLable2) and self.isLive2:
                print('Sudaaar')
                self.Lives2 = self.Lives2 - 1
                self.player2lives.setText('Lives: ' + str(self.Lives2))
                #barrel.move(0,0)
                barrel.hide()
                self.barrels.remove(barrel)
                if (self.Lives2 > 0):
                    self.avatarLable2.move(720, 545)
                else:
                    self.isLive2 = False
                    self.avatarLable2.clear()
                    self.avatarLable2.move(1100, 1100)
        self.isGameOver()

    def isHit(self, first, second):
        rec1 = first.geometry()
        y1 = first.height()
        x1 = first.width()
        rec2 = second.geometry()
        x2 = second.width()
        y2 = second.height()
        if rec1.x() + x1 in range(rec2.x(), rec2.x() + x2):
            if rec1.y() in range(rec2.y(), rec2.y() + y2):
                return True
            elif rec1.y() + y1 in range(rec2.y(), rec2.y() + y2):
                return True

        if rec1.x() in range(rec2.x(), rec2.x() + x2):
            if rec1.y() in range(rec2.y(), rec2.y() + y2):
                return True
            elif rec1.y() + y1 in range(rec2.y(), rec2.y() + y2):
                return True

        if rec2.x() + x2 in range(rec1.x(), rec1.x() + x1):
            if rec2.y() in range(rec1.y(), rec1.y() + y1):
                return True
            elif rec2.y() + y2 in range(rec1.y(), rec1.y() + y1):
                return True

        if rec2.x() in range(rec1.x(), rec1.x() + x1):
            if rec2.y() in range(rec1.y(), rec1.y() + y1):
                return True
            elif rec2.y() + y2 in range(rec1.y(), rec1.y() + y1):
                return True


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

        if key == Qt.Key_Right and self.isLive1:
            if rect.x() < 755:
                if rect.y() == 545 or rect.y() == 455 or rect.y() == 365 or rect.y() == 275 or rect.y() == 185:
                    self.movePlayerFlags = 1
                    self.moveRight()
        elif key == Qt.Key_Left and self.isLive1:
            if rect.x() > 20:
                if rect.y() == 545 or rect.y() == 455 or rect.y() == 365 or rect.y() == 275 or rect.y() == 185:
                    self.movePlayerFlags = 1
                    self.moveLeft()
        elif key == Qt.Key_Up and self.isLive1:
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
        elif key == Qt.Key_Down and self.isLive1:
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
        elif key == Qt.Key_A  and self.isLive2:
            if rect2.x() > 20:
                if rect2.y() == 545 or rect2.y() == 455 or rect2.y() == 365 or rect2.y() == 275 or rect2.y() == 185:
                    self.movePlayerFlags = 2
                    self.moveLeft()
        elif key == Qt.Key_D and self.isLive2:
            if rect2.x() < 755:
                if rect2.y() == 545 or rect2.y() == 455 or rect2.y() == 365 or rect2.y() == 275 or rect2.y() == 185:
                    self.movePlayerFlags = 2
                    self.moveRight()
        elif key == Qt.Key_W and self.isLive2:
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
        elif key == Qt.Key_S and self.isLive2:
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
        self.monkey_movement.die()
        self.barrel_movement.die()
        self.points_counter.die()
        self.unexpected_force.die()
        self.delayed_effect_of_force.die()
        self.unexpected_force_life.quit()
        self.unexpected_force_bomb.quit()

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
        elif nivo <= 273 + dodatak and nivo >= 251 + dodatak:
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
            self.point1 = 0 + self.pamtiPrvog
            self.first[0] = False
        elif self.first[1] == True:
            self.point1 = 1 + self.pamtiPrvog
            self.first[1] = False
        elif self.first[2] == True:
            self.point1 = 2 + self.pamtiPrvog
            self.first[2] = False
        elif self.first[3] == True:
            self.point1 = 3 + self.pamtiPrvog
            self.first[3] = False
        elif self.first[4] == True:
            self.point1 = 4 + self.pamtiPrvog
            self.first[4] = False
        elif self.first[5] == True:
            self.point1 = 5 + self.pamtiPrvog
            self.first[5] = False
            self.pamtiPrvog = self.point1
            self.pamtiDrugog = self.point2
            self.newLevel()
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
            self.point2 = 0 + self.pamtiDrugog
            self.second[0] = False
        elif self.second[1] == True:
            self.point2 = 1 + self.pamtiDrugog
            self.second[1] = False
        elif self.second[2] == True:
            self.point2 = 2 + self.pamtiDrugog
            self.second[2] = False
        elif self.second[3] == True:
            self.point2 = 3 + self.pamtiDrugog
            self.second[3] = False
        elif self.second[4] == True:
            self.point2 = 4 + self.pamtiDrugog
            self.second[4] = False
        elif self.second[5] == True:
            self.point2 = 5 + self.pamtiDrugog
            self.second[5] = False
            self.pamtiDrugog = self.point2
            self.pamtiPrvog = self.point1
            self.newLevel()
        else:
            self.point2 = self.point2

        self.player1score.setText('Score: ' + str(self.point1))
        self.player2score.setText('Score: ' + str(self.point2))

    def showLifeForce(self):
        self.forceLife = QLabel(self)
        forceLifeImage = QPixmap('Assets/Heart/Life.png')
        self.forceLife.setStyleSheet('QLabel { background-color: transparent }')
        forceLifeImageCropped = forceLifeImage.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.forceLife.setPixmap(QPixmap(forceLifeImageCropped))

        randX = random.randrange(15, 765)
        randY = random.randrange(0, 4)

        nivoi = [565, 475, 385, 295, 205]
        positionY = nivoi[randY]
        self.forceLife.move(randX, positionY)
        self.forceLife.show()

        self.LifeExist = True

    def hideLifeForce(self):
        self.forceLife.clear()
        self.LifeExist = False

    def showBombForce(self):
        self.forceBomb = QLabel(self)
        forceBombImage = QPixmap('Assets/Heart/FlameBomb.png')
        self.forceBomb.setStyleSheet('QLabel { background-color: transparent }')
        forceBombImageCropped = forceBombImage.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.forceBomb.setPixmap(QPixmap(forceBombImageCropped))

        randX = random.randrange(15, 765)
        randY = random.randrange(0, 4)

        nivoi = [565, 475, 385, 295, 205]
        positionY = nivoi[randY]
        self.forceBomb.move(randX, positionY)
        self.forceBomb.show()

        self.bombExist = True

    def hideBombForce(self):
        self.forceBomb.clear()
        self.bombExist = False

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def newLevel(self):
        self.level = self.level + 1
        self.levelLabel.setText('Level ' + str(self.level))

        self.monkeyLabel.move(375, 155)
        self.avatarLable.move(40, 545)
        self.avatarLable2.move(720, 545)

        self.monkey_movement.die()
        self.barrel_movement.die()

        for b in self.barrels:
            b.hide()
            #self.barrels.remove(b)

        self.barrels.clear()
        '''
        image1 = QPixmap('Assets/Brick/Platforma.png')
        image2 = QPixmap('Assets/Brick/BluePlatform.png')
        image3 = QPixmap('Assets/Brick/RedPlatform.png')

        sirina = 800 / 54

        for p in self.PlatformList:
            p.hide()

        self.PlatformList.clear()

        if self.level % 3 == 1:
            croppedImage = image1.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)

            for i in range(1, 6):
                for j in range(38):
                    self.PlatformList.append(self.setPlatform(croppedImage, i, j, sirina))

                self.PlatformList.append(self.setPlatform(croppedImage, i, 38, sirina))

        elif self.level % 3 == 2:
            croppedImage = image2.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)

            for i in range(1, 6):
                for j in range(38):
                    self.PlatformList.append(self.setPlatform(croppedImage, i, j, sirina))

                self.PlatformList.append(self.setPlatform(croppedImage, i, 38, sirina))

        else:
            croppedImage = image3.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.FastTransformation)

            for i in range(1, 6):
                for j in range(38):
                    self.PlatformList.append(self.setPlatform(croppedImage, i, j, sirina))

                self.PlatformList.append(self.setPlatform(croppedImage, i, 38, sirina))'''

        self.avatarLable.show()
        self.avatarLable2.show()

        #self.monkey_movement.move_monkey_signal.connect(self.moveMonkey)
        self.monkey_movement.start(self.level)

        #self.barrel_movement.move_barrel_signal.connect(self.moveBarrel)
        self.barrel_movement.start(self.level)

    def isGameOver(self):
        if self.Lives1 > 0 and self.Lives2 == 0:
            self.pobednik = 1
        elif self.Lives1 == 0 and self.Lives2 > 0:
            self.pobednik = 2
        elif self.Lives1 == 0 and self.Lives2 == 0:
            #gameOver(self.pobdnik)
            #print("Pobednik: " + str(self.pobednik))
            winnerName = ""
            score = 0
            if self.pobednik == 1:
                winnerName = self.nameOne
                score = self.point1
            elif self.pobednik == 2:
                winnerName = self.nameTwo
                score = self.point2

            self.gameOver = GameOver(winnerName, score)
            self.close()

    def checkCollisionWithUnexpectedForce(self):
        if self.LifeExist:
            if self.isHit(self.forceLife, self.avatarLable):
                self.unexpected_force.forces[0] = True
                self.forceLife.clear()
                #self.delayed_effect_of_force.start()
                self.LifeExist = False

        if self.bombExist:
            if self.isHit(self.forceBomb, self.avatarLable):
                self.unexpected_force.forces[1] = True
                self.forceBomb.clear()
                self.bombExist = False

        if self.LifeExist:
            if self.isHit(self.forceLife, self.avatarLable2):
                self.unexpected_force.forces[2] = True
                self.forceLife.clear()
                self.LifeExist = False

        if self.bombExist:
            if self.isHit(self.forceBomb, self.avatarLable2):
                self.unexpected_force.forces[3] = True
                self.forceBomb.clear()
                self.bombExist = False

    def executeForce(self, force):
        if force == 1:
            self.Lives1 = self.Lives1 + 1
            self.player1lives.setText('Lives: ' + str(self.Lives1))
            print(str(self.Lives1))
        elif force == 2:
            self.Lives1 = self.Lives1 - 1
            self.player1lives.setText('Lives: ' + str(self.Lives1))
            print(str(self.Lives1))

            if self.Lives1 > 0:
                self.avatarLable.move(40, 545)
            else:
                self.isLive1 = False
                self.avatarLable.clear()
                self.avatarLable.move(1100, 1100)

            self.isGameOver()

    def executeForce2(self, force):
        if force == 1:
            self.Lives2 = self.Lives2 + 1
            self.player2lives.setText('Lives: ' + str(self.Lives2))
        elif force == 2:
            self.Lives2 = self.Lives2 - 1
            self.player2lives.setText('Lives: ' + str(self.Lives2))

            if self.Lives2 > 0:
                self.avatarLable2.move(720, 545)
            else:
                self.isLive2 = False
                self.avatarLable2.clear()
                self.avatarLable2.move(1100, 1100)

            self.isGameOver()


