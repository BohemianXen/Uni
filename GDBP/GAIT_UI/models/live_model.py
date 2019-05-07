from PyQt5.QtCore import QObject, pyqtSignal
from application.Logger import Logger
import struct

class LiveModel(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._motion_data = []

    @property
    def motion_data(self):
        return self._motion_data

    def add_motion_data(self, new_data):
        int_data = []
        for val in new_data:
            uint_val = int(val, 2).to_bytes(1, byteorder='big')
            int_val = struct.unpack('b', uint_val)[0]
            int_data.append(int_val)

        self._motion_data.append(int_data)

    def reset_data(self):
        self._motion_data = []
