from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool
from application.Logger import Logger
from controllers.connect_manager.DeviceFinder import DeviceFinder


class ConnectController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)

        self._device_finder = DeviceFinder()
        self._device_finder.signals.searchComplete.connect(self.search_complete)
        self._devices_found = {}

        self.pool = QThreadPool.globalInstance()

    def link_view(self, view):
        self._view = view

    # slot implementations for view signals
    @pyqtSlot()
    def search_button_clicked(self):
        self._view.toggle_search_button(value=False)
        self._view.toggle_connect_button(value=False)
        self.pool.start(self._device_finder)
        # print(self.pool.activeThreadCount())

    @pyqtSlot(dict)
    def search_complete(self, devices):
        self._devices_found = devices
        if len(self._devices_found) != 0:
            for name, address in self._devices_found.items():
                self._view.update_devices(name)
        else:
            self._logger.log("No bluetooth devices found", Logger.DEBUG)
            self._view.update_no_devices()

        self._view.toggle_search_button(True)  # Suspect this will be useless once threading

    @pyqtSlot()
    def connect_button_clicked(self, device):
        self._logger.log("Attempting to connect to {} device selected".format(device), Logger.DEBUG)

    # TODO: multi-selection if pairing to multiple devices?
    @pyqtSlot()
    def selection_changed(self, selected):
        self._logger.log("Device {} selected".format(self._view.get_text(selected)), Logger.DEBUG)
        self._view.toggle_connect_button(value=True)
