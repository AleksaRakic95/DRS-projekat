from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time


class BarrelMovement(QObject):
    move_barrel_signal = pyqtSignal()

    def __init__(self, level):
        super().__init__()

        self.level = level

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def die(self):
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        while True:
            self.move_barrel_signal.emit()
            time.sleep(0.07 - self.level * 0.0005)