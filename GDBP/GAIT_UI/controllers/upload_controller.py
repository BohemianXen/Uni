from PyQt5.QtCore import QObject, pyqtSlot
from application.Logger import Logger


class UploadController(QObject):
    """ Controller class. Handles the core program logic and data transfer between its view and model counterparts.

    Args:
        model (QWidget): The controller's corresponding model.

    Parameters:
        _model (QWidget): A reference to the passed model.
        _view (QWidget): A reference to this controller's corresponding view.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)

    def link_view(self, view):
        self._view = view

    def unlock_view(self):
        """Unlocks view on succesful device connection."""
        self._view.unlock_view()
