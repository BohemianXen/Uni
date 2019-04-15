from PyQt5.QtCore import QObject, pyqtSlot


class ConnectController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

    def link_view(self, view):
        self._view = view
