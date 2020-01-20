from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time

class PointsCounter(QObject):
    point_counter_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

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
            self.point_counter_signal.emit()
            time.sleep(0.2)

'''import time
import random

from multiprocessing import Pipe, Process

from Board import position1


class PointsCounter(Process):
    def __init__(self, pipe: Pipe):
        super().__init__(target=self.move_enemies, args=[pipe])

    def poeni(self, pipe: Pipe):
        while True:
            #print("TREBALO BI DRUGI->", multiprocessing.current_process().pid)
            if position1 == True:'''
