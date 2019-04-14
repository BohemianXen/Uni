from PyQt5.QtCore import QObject, pyqtSignal


class MainModel(QObject):
    def __init__(self):
        super().__init__()
