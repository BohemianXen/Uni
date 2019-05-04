from PyQt5.QtCore import QObject, pyqtSignal
from application.Logger import Logger


class DeviceModel(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)
