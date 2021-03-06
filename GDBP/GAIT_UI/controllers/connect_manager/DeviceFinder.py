from PyQt5.QtCore import pyqtSignal, QRunnable, QObject
from application.Logger import Logger
from bluetooth import discover_devices, BluetoothError
import traceback


class DeviceFinderSignals(QObject):
    searchComplete = pyqtSignal(dict)

    def __init__(self):
        super(DeviceFinderSignals, self).__init__()


# TODO: Add checks for own bluetooth chip
class DeviceFinder(QRunnable):
    """PyBluez class for connecting to the device. Currently scans services.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        signals (DeviceConnectorSignals): The signals associated with this class.
    """

    def __init__(self):
        super(DeviceFinder, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DeviceFinderSignals()

    def run(self):
        """Overrides the QRunnable implementation to start a device search thread."""
        self._logger.log('Starting new thread; searching for devices', Logger.DEBUG)
        devices_found = {}

        try:
            discovered_devices = discover_devices(lookup_names=True)  # discover nearby/paired devices

            # places discovered devices into a dictionary in address: name format
            for (address, name) in discovered_devices:
                devices_found[address] = name
                self._logger.log('Found bluetooth device with name: {} and address: {}'.format(name, address),
                                 Logger.DEBUG)
        except BluetoothError as error:
            self._logger.log(str(error), Logger.DEBUG)
        except OSError:
            self._logger.log('Exception encountered while searching for devices', Logger.DEBUG)
            self._logger.log(traceback.format_exc(), Logger.DEBUG)

        self._logger.log('Search complete, deleting thread', Logger.DEBUG)
        self.signals.searchComplete.emit(devices_found)
