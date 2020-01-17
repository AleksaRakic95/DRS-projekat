from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time

class UnexpectedForce(QObject):
    mario1_signal = pyqtSignal(int)
    mario2_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.forces = [False, False, False, False]
        self.is_done = False

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.is_done = False
        self.thread.start()

    def die(self):
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        while not self.is_done:
            if self.forces[0]:
                time.sleep(2)
                self.mario1_signal.emit(1)
                self.forces[0] = False
            elif self.forces[1]:
                time.sleep(2)
                self.mario1_signal.emit(2)
                self.forces[1] = False

            if self.forces[2]:
                time.sleep(2)
                self.mario2_signal.emit(1)
                self.forces[2] = False
            elif self.forces[3]:
                time.sleep(2)
                self.mario2_signal.emit(2)
                self.forces[3] = False

            time.sleep(0.1)