from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time

class PointsCounter(QObject):
    point_counter_signal = pyqtSignal()

    def __init__(self):
        super().__init__()


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
            self.point_counter_signal.emit()
            time.sleep(0.2)