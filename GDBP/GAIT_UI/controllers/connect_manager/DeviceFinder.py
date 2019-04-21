from PyQt5.QtCore import pyqtSignal, QRunnable, QObject
from application.Logger import Logger
import bluetooth


class DeviceFinderSignals(QObject):
    searchComplete = pyqtSignal(dict)

    def __init__(self):
        super(DeviceFinderSignals, self).__init__()


# TODO: Add checks for own bluetooth chip
class DeviceFinder(QRunnable):
    def __init__(self):
        super(DeviceFinder, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DeviceFinderSignals()

    # TODO: Handle exception raised and handle duplicate names
    def run(self):
        self._logger.log("Starting new thread", Logger.DEBUG)
        devices_found = {}

        try:
            discovered_devices = bluetooth.discover_devices(lookup_names=True)
            for (address, name) in discovered_devices:
                devices_found[address] = name
                self._logger.log("Found bluetooth device with name: {} and address: {}".format(name, address),
                                 Logger.DEBUG)
        except bluetooth.BluetoothError as error:
            self._logger.log(str(error), Logger.ERROR)

        self.signals.searchComplete.emit(devices_found)
        self._logger.log("Deleting thread", Logger.DEBUG)
