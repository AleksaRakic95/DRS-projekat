from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor, QIcon, QPixmap
import sys


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Donkey Kong")

        lay = QVBoxLayout()

        label = QLabel(self)
        pixmap = QPixmap('C:/Users/Aleksa/Desktop/Assets/DonekyKongLogo.jpg')
        label.setPixmap(pixmap)
        self.resize(200, 400)

        lay.addWidget(label)
        self.show()
