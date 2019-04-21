from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from application.Logger import Logger


class HomeController(QObject):

    # signals for view navigation that are handled by main controller
    connectClicked = pyqtSignal(str)
    liveClicked = pyqtSignal(str)
    uploadClicked = pyqtSignal(str)
    historyClicked = pyqtSignal(str)
    deviceClicked = pyqtSignal(str)
    accountClicked = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None
        self.name = __class__.__name__
        self._logger = Logger(self.name)

    def link_view(self, view):
        self._view = view

    # slot implementations for model signals
    @pyqtSlot(str)
    def connect_clicked(self):
        self._logger.log("Connect button clicked", Logger.DEBUG)
        self.connectClicked.emit('connect')

    @pyqtSlot(str)
    def live_clicked(self):
        self.liveClicked.emit('live')

    @pyqtSlot(str)
    def upload_clicked(self):
        self.uploadClicked.emit('upload')

    @pyqtSlot(str)
    def history_clicked(self):
        self.historyClicked.emit('history')

    @pyqtSlot(str)
    def device_clicked(self):
        self.deviceClicked.emit('device')

    @pyqtSlot(str)
    def account_clicked(self):
        self.accountClicked.emit('account')
