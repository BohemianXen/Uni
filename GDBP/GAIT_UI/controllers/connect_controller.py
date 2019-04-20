from PyQt5.QtCore import QObject, pyqtSlot
from application.Logger import Logger


class ConnectController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)

    def link_view(self, view):
        self._view = view
