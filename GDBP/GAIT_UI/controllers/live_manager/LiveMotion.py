from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QTimer
from application.Logger import Logger
import numpy.random as random
import time


class LiveMotionSignals(QObject):
    dataReady = pyqtSignal(str, float)

    def __init__(self):
        super(LiveMotionSignals, self).__init__()


class LiveMotion(QRunnable):
    def __init__(self):
        super(LiveMotion, self).__init__()

        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = LiveMotionSignals()

        self.plotting = False

    @property
    def plotting(self):
        return self._plotting

    @plotting.setter
    def plotting(self, value):
        self._plotting = value

    def run(self):
        self._logger.log('Starting new thread; live plotting motion data', Logger.DEBUG)
        self.plotting = True

        while self.plotting:
            data = self.get_data()
            self.signals.dataReady.emit('motion', data)
            time.sleep(0.5)

        self._logger.log('Deleting live motion thread', Logger.DEBUG)

    @staticmethod
    def get_data():
        return random.rand()
