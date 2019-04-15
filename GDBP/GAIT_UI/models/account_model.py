from PyQt5.QtCore import QObject, pyqtSignal


class AccountModel(QObject):
    def __init__(self):
        super().__init__()
