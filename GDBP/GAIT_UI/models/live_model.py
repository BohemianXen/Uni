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

        self._uv_data = []
        self._motion_data = []
        self._steps = 0
        self._freefall = False
        self._sig_motion = False

    @property
    def uv_data(self):
        return self._uv_data

    def add_uv_data(self, new_data):
        self._uv_data.append(new_data)

    @property
    def motion_data(self):
        return self._motion_data

    def add_motion_data(self, type, new_data):
        """Converts new raw binary string samples into signed int values and stores them."""
        data = []
        if type == 0:  # convert byte to signed int
            for val in new_data:
                uint_val = int(val, 2).to_bytes(1, byteorder='big')  # raw data was stored in big endian order
                int_val = struct.unpack('b', uint_val)[0]
                data.append(int_val)
        else:  # convert serial print to float
            data = new_data

        self._motion_data.append(data)  # add latest sample to the older ones

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, val):
        self._steps = val

    @property
    def freefall(self):
        return self._freefall

    @freefall.setter
    def freefall(self, val):
        self._freefall = val

    @property
    def sig_motion(self):
        return self._sig_motion

    @sig_motion.setter
    def sig_motion(self, val):
        self._sig_motion = val


    def reset_data(self):
        self._uv_data = []
        self._motion_data = []
        self.steps = 0
        self.freefall = False
        self.sig_motion = False
