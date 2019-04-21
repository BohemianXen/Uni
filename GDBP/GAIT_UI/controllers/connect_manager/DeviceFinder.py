from PyQt5.QtCore import QTimer
from application.Logger import Logger
import bluetooth


# TODO: Add checks for own bluetooth chip
class DeviceFinder:
    def __init__(self):
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self._devices_found = {}

    # TODO: Handle exception raised and handle duplicate names
    def search(self):
        try:
            # timer = QTimer(self.agent)
            # timer.start(500)
            discovered_devices = bluetooth.discover_devices(lookup_names=True)
        except bluetooth.BluetoothError():
            self._logger.log('Unable to establish local bluetooth device', self._logger.ERROR)

        for (address, name) in discovered_devices:
            self._devices_found[name] = address
            self._logger.log("Found bluetooth device with name: {} and address: {}".format(name, address),
                             self._logger.DEBUG)

        return self._devices_found


    def return_devices(self):
        return self._devices_found
