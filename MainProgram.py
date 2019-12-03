# MainProject

# Dejina linija koda

from PyQt5.QtWidgets import QApplication
import sys

from Board import Board
from StartWindow import StartWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = StartWindow()
    sys.exit(app.exec_())