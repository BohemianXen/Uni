from PyQt5.QtCore import QObject, pyqtSignal
from application.Logger import Logger


class ConnectModel(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        _devices_found (dict): A dictionary of the nearby bluetooth devices found (address: name).
        _target_device (tuple): The user selected device, held in a 2D tuple.
    """

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._devices_found = {}
        self._target_device = ()
        self._max_attempts = 3

    @property
    def devices_found(self):
        """Gets the dictionary of found devices."""
        return self._devices_found

    @devices_found.setter
    def devices_found(self, devices):
        self._devices_found = devices

    @property
    def target_device(self):
        """Gets the user selected target device."""
        return self._target_device

    @target_device.setter
    def target_device(self, device):
        self._target_device = device

    @property
    def max_attempts(self):
        """Gets the max connection attempts allowed."""
        return self._max_attempts
