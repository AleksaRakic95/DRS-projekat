from PyQt5.QtCore import QThread, pyqtSignal

import time
import random

class UnexpectedForceLife(QThread):

    show_life_signal = pyqtSignal()
    hide_life_signal = pyqtSignal()

    def __init__(self, parent):
        QThread.__init__(self, parent)

    def run(self):
        while True:
            rand_sleep = random.randrange(5,10)
            time.sleep(rand_sleep)
            self.show_life_signal.emit()
            time.sleep(5)
            self.hide_life_signal.emit()