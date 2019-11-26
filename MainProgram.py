# MainProject

# Dejina linija koda
#Commit

from PyQt5.QtWidgets import QApplication
import sys

from Board import Board


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board()
    sys.exit(app.exec_())