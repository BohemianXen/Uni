from PyQt5.QtCore import QObject, pyqtSlot
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
        self._devices_found = {}


    def link_view(self, view):
        self._view = view

    # slot implementations for view signals
    @pyqtSlot()
    def search_button_clicked(self):
        self._devices_found = self._device_finder.search()
        if len(self._devices_found) != 0:
            for name, address in self._devices_found.items():
                self._view.update_devices(name)
        else:
            self._logger.log("No bluetooth devices found", self._logger.DEBUG)
            self._view.update_no_devices()

    @pyqtSlot()
    def connect_button_clicked(self, device):
        self._logger.log("Attempting to connect to {} device selected".format(device), self._logger.DEBUG)

    # TODO: multi-selection if pairing to multiple devices?
    @pyqtSlot()
    def selection_changed(self, selected):
        self._logger.log("Device {} selected".format(self._view.get_text(selected)), self._logger.DEBUG)
        self._view.toggle_connect_button(True)
