from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time


class BarrelMovement(QObject):
    move_barrel_signal = pyqtSignal()

    def __init__(self, level):
        super().__init__()

        self.level = level
        self.is_done = False

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def die(self):
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        while not self.is_done:
            self.move_barrel_signal.emit()
            time.sleep(0.07 - self.level * 0.0005)