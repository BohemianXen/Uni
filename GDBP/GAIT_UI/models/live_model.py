from PyQt5.QtCore import QObject, pyqtSignal


class LiveModel(QObject):
    def __init__(self):
        super().__init__()
