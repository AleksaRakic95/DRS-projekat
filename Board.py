from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget
from PyQt5.QtGui import QColor, QPixmap, QMovie, QPainter, QFont
from PyQt5.QtCore import Qt, QByteArray
import sys, time
from key_notifyer import KeyNotifyer


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

        self.initBoard()

        self.key_notifyer = KeyNotifyer()
        self.key_notifyer.key_signal.connect(self.__update_position__)
        self.key_notifyer.start()

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

        self.PlatformList = []

        for i in range(1, 6):
            for j in range(38):
                self.PlatformList.append(self.setPlatform(platformImageCropped, i, j, sirina))

        '''self.ladderlabel = QLabel(self)
        ladderImage = QPixmap('Assets/Ladder/ladder.png')
        ladderImageCropped = ladderImage.scaled(30, 70, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.ladderlabel.setPixmap(QPixmap(ladderImageCropped))
        self.ladderlabel.move(685,515)'''

        self.setPrincess()
        self.playerName()
        self.setLadder()
        #self.setBarrel()
        self.setAvatars("Assets/Mario/marioR.png", "Assets/Mario/mario2L.png")

        self.show()

    def playerName(self):
        self.playerOne = QLabel(self)
        fontLbl = QFont()
        fontLbl.setFamily("Arcade Normal")
        fontLbl.setPointSize(8)
        self.playerOne.setText(self.nameOne)
        self.playerOne.setFont(fontLbl)
        self.playerOne.setStyleSheet("QLabel {color: white}")
        self.playerOne.move(20,20)

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

    '''def setBarrel(self):
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

        self.FourBurrellabel = QLabel(self)
        barrel4Image = QPixmap('Assets/Barrel/Burrel4.png')
        barrel4ImageCropped = barrel4Image.scaled(50, 70, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.FourBurrellabel.setPixmap(QPixmap(barrel4ImageCropped))
        self.FourBurrellabel.move(25, 155)'''

    def setAvatars(self, naziv, naziv2):
        ''' Avatar 1 '''

        self.avatarLable = QLabel(self)
        avatarImage = QPixmap(naziv)
        self.avatarLable.setStyleSheet('QLabel { background-color: transparent }')
        avatarImageCropped = avatarImage.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarLable.setPixmap(QPixmap(avatarImageCropped))
        self.avatarLable.move(100, 545)

        ''' Avatar 2 '''

        self.avatarLable2 = QLabel(self)
        avatarImage2 = QPixmap(naziv2)
        self.avatarLable2.setStyleSheet('QLabel { background-color: transparent }')
        avatarImageCropped2 = avatarImage2.scaled(30, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarLable2.setPixmap(QPixmap(avatarImageCropped2))
        self.avatarLable2.move(500, 545)

    def keyPressEvent(self, event):
        self.key_notifyer.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifyer.remove_key(event.key())

    def __update_position__(self, key):
        rect  = self.avatarLable.geometry()
        rect2 = self.avatarLable2.geometry()

        if key == Qt.Key_Right:
            if rect.x() < 755:
                self.movePlayerFlags = 1
                self.moveRight()
        elif key == Qt.Key_Left:
            if rect.x() > 20:
                self.movePlayerFlags = 1
                self.moveLeft()
        elif key == Qt.Key_Up:
            self.movePlayerFlags = 1
            self.moveUp()
        elif key == Qt.Key_Down:
            self.movePlayerFlags = 1
            self.moveDown()
        elif key == Qt.Key_A:
            if rect2.x() > 20:
                self.movePlayerFlags = 2
                self.moveLeft()
        elif key == Qt.Key_D:
            if rect2.x() < 755:
                self.movePlayerFlags = 2
                self.moveRight()
        elif key == Qt.Key_W:
            self.movePlayerFlags = 2
            self.moveUp()
        elif key == Qt.Key_S:
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
            if x == 684:
                return True
        elif nivo <= 453 + dodatak and nivo >= 365 + dodatak:
            if x == 84 or x == 396:
                return True
        elif nivo <= 363 + dodatak and nivo >= 275 + dodatak:
            if x == 196 or x == 612:
                return True
        elif nivo <= 273 + dodatak and nivo >= 185 + dodatak:
            if x == 700:
                return True
        elif nivo <= 183 + dodatak and nivo >= 95 + dodatak:
            if x == 380:
                return True

        ''' Move down on broken Ladder '''

        if nivo <= 543 + dodatak and nivo >= 521 + dodatak:
            if x == 332:
                return True
        elif nivo <= 363 + dodatak and nivo >= 341 + dodatak:
            if x == 468:
                return True
        elif nivo <= 273 + dodatak and nivo >= 249 + dodatak:
            if x == 324:
                return True

        return False
    '''
    def setAvatarMove(self, naziv):
        avatarImage = QPixmap(naziv)
        avatarImageCropped = avatarImage.scaled(30,40, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.avatarLable.setPixmap(QPixmap(avatarImageCropped))

    def keyPressEvent(self, event):
        #super(Board, self).kretanje(event)
        key = event.key()

        self.brojac = 5

        if key == Qt.Key_Right:
            if self.PocetnaDimenzija < 755:
                self.setAvatarMove("Assets/Mario/right.png")
                self.PocetnaDimenzija = self.PocetnaDimenzija + self.brojac;
                self.avatarLable.move(self.PocetnaDimenzija, 545)
        elif key == Qt.Key_Left:
            if self.PocetnaDimenzija > 81:
                self.PocetnaDimenzija = self.PocetnaDimenzija - self.brojac;
                #self.avatarLable.move(self.PocetnaDimenzija, 545)
                self.setAvatarMove("Assets/Mario/left.png")
                self.avatarLable.move(self.PocetnaDimenzija, 545)
    
        elif key == Qt.Key_Space:
            self.jump()'''

    '''def jump(self):
        self.isJump = 1
        self.update()'''

    def update(self):
        if self.isJump:
            if self.v > 0:
                F = (0.5 * self.m * (self.v * self.v))
            else:
                F = -(0.5 * self.m * (self.v * self.v))
            self.y = self.y - F
            self.v = self.v - 1

            self.avatarLable.move(self.PocetnaDimenzija, self.y)

            if self.y >= 545:
                self.y = 545
                self.avatarLable.move(self.PocetnaDimenzija, self.y)
                self.isJump = 0
                self.v = 3

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


    '''
    def keyPressEvent(self, event):
        key = event.key()

        self.step = 5

        if key == Qt.Key_Right:
            if self.startingPositionOne < 755:
                self.setAvatarOneMove("Assets/Mario/right.png")
                self.startingPositionOne = self.startingPositionOne + self.step
                self.avatarOneLbl.move(self.startingPositionOne, 545)
        elif key == Qt.Key_Left:
            if self.startingPositionOne > 81:
                self.startingPositionOne = self.startingPositionOne - self.step
                self.setAvatarOneMove("Assets/Mario/left.png")
                self.avatarOneLbl.move(self.startingPositionOne, 545)
        elif key == Qt.Key_D:
            if self.startingPositionTwo < 755:
                self.setAvatarTwoMove("Assets/Mario/right.png")
                self.startingPositionTwo = self.startingPositionTwo + self.step
                self.avatarTwoLbl.move(self.startingPositionTwo, 545)
        elif key == Qt.Key_A:
            if self.startingPositionTwo > 81:
                self.startingPositionTwo = self.startingPositionTwo - self.step
                self.setAvatarTwoMove("Assets/Mario/left.png")
                self.avatarTwoLbl.move(self.startingPositionTwo, 545)
        '''

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
