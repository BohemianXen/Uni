from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QTimer
from application.Logger import Logger
import numpy.random as random
import time
from os import getcwd


class LiveMotionSignals(QObject):
    dataReady = pyqtSignal(str, list)

    def __init__(self):
        super(LiveMotionSignals, self).__init__()


class LiveMotion(QRunnable):
    def __init__(self):
        super(LiveMotion, self).__init__()

        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = LiveMotionSignals()
        self.dummy_file = getcwd()[:getcwd().rfind('\\') + 1]
        self.dummy_file += r'resources\dummy_files\motion.txt'
        self.sample_rate = 100  # Hz
        self.plotting = False
        self.data = []

    @property
    def plotting(self):
        return self._plotting

    @plotting.setter
    def plotting(self, value):
        self._plotting = value

    def run(self):
        self._logger.log('Starting new thread; live plotting motion data', Logger.DEBUG)
        self.plotting = True
        with open(self.dummy_file) as f:
            while self.plotting:
                line = f.readline()
                if line != '\n':
                    self.data.append(line)
                else:
                    data = self.data.copy()
                    self.signals.dataReady.emit('motion', data)
                    self.data = []
                time.sleep(1/self.sample_rate)

        self._logger.log('Deleting live motion thread', Logger.DEBUG)

    @staticmethod
    def get_data():
        return random.rand()
