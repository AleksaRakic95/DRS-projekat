from PyQt5.QtCore import QThread, pyqtSignal

import time
import random


class UnexpectedForceBomb(QThread):
    show_bomb_signal = pyqtSignal()
    hide_bomb_signal = pyqtSignal()

    def __init__(self, parent):
        QThread.__init__(self, parent)

    def run(self):
        while True:
            rand_sleep = random.randrange(5, 10)
            time.sleep(rand_sleep)
            self.show_bomb_signal.emit()
            time.sleep(7)
            self.hide_bomb_signal.emit()
