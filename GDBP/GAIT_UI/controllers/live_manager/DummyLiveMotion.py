from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QTimer
from application.Logger import Logger
import numpy.random as random
import time
from os import getcwd


class DummyLiveMotionSignals(QObject):
    dataReady = pyqtSignal(str, list)
    dataFinished = pyqtSignal(str)

    def __init__(self):
        super(DummyLiveMotionSignals, self).__init__()


class DummyLiveMotion(QRunnable):
    """Reads in dummy live data from text file one line at a time.

    Parameters:
        _view (QWidget): A reference to this controller's corresponding view.
        name (str): The name of this class.
        signals (DeviceConnectorSignals): The signals associated with this class.
        dummy_file (string): Filename with the dummy data.
        sample_rate (int): Line read rate (approximate).
        plotting (bool): Flag to stop plotting from the main thread.
    """

    def __init__(self):
        super(DummyLiveMotion, self).__init__()

        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DummyLiveMotionSignals()
        self.dummy_file = getcwd()[:getcwd().rfind('\\') + 1]
        self.dummy_file += r'resources\dummy_files\motion.txt'
        self.sample_rate = 100  # Hz
        self._streaming = False
        self.data = []

    @property
    def streaming(self):
        return self._streaming

    @streaming.setter
    def streaming(self, value):
        self._streaming = value

    def run(self):
        """Overrides the QRunnable implementation to start a dummy motion thread."""
        self._logger.log('Starting new thread; plotting dummy motion data', Logger.DEBUG)
        self.streaming = True

        with open(self.dummy_file) as f:
            line = None
            while self.streaming and line != '':
                line = f.readline()
                if line != '\n':
                    self.data.append(line)
                else:
                    data = self.data.copy()
                    self.signals.dataReady.emit('dummy motion', data)
                    self.data = []
                time.sleep(1/1000)  # self.sample_rate) TODO: Find a working maximum for test purposes.

        self.signals.dataFinished.emit('dummy motion')
        self._logger.log('Deleting dummy motion thread', Logger.DEBUG)

    @staticmethod
    def get_data():
        return random.rand()
