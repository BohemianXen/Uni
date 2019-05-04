from PyQt5.QtCore import QObject, pyqtSignal
from application.Logger import Logger


class MainModel(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        _views (dict): A dictionary of all child views.
        _controllers (dict): A dictionary of all child controllers.
    """

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._views = {
            'login': None,
            'home': None,
            'connect': None,
            'live': None,
            'upload': None,
            'history': None,
            'device': None,
            'account': None
        }

        self._controllers = self._views.copy()

    @property
    def views(self):
        """Gets the dictionary of all views."""
        return self._views

    @views.setter
    def views(self, views):
        self._views = views

    @property
    def controllers(self):
        """Gets the dictionary of all controllers."""
        return self._controllers

    @controllers.setter
    def controllers(self, controllers):
        self._controllers = controllers
