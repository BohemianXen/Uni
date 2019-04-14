from PyQt5.QtCore import QObject, pyqtSlot


class HomeController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model