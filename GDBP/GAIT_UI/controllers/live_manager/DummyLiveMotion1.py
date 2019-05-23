from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QTimer
from application.Logger import Logger
import numpy.random as random
import time
from os import getcwd


class DummyLiveMotion1Signals(QObject):
    dataReady = pyqtSignal(list)
    done = pyqtSignal(str)

    def __init__(self):
        super(DummyLiveMotion1Signals, self).__init__()


class DummyLiveMotion1(QRunnable):
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
        super(DummyLiveMotion1, self).__init__()

        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DummyLiveMotion1Signals()
        self.dummy_file = getcwd()[:getcwd().rfind('\\') + 1]
        self.dummy_file += r'resources\dummy_files\sensors.txt'
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
                    self.signals.dataReady.emit(data[:28])
                    self.data = []
                time.sleep(1/100)  # self.sample_rate) TODO: Find a working maximum for test purposes.

        self.signals.done.emit('live motion')
        self._logger.log('Deleting dummy motion thread', Logger.DEBUG)

    @staticmethod
    def get_data():
        return random.rand()
