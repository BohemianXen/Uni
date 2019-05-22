from PyQt5.QtCore import pyqtSignal, QRunnable, QObject
from application.Logger import Logger
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent
# import traceback
from PyQt5.QtTest import QSignalSpy


class DeviceFinderSignals(QObject):
    searchComplete = pyqtSignal(dict)

    def __init__(self):
        super(DeviceFinderSignals, self).__init__()


# TODO: Add checks for own bluetooth chip
class DeviceFinder(QRunnable):
    """Qt Bluetooth class for connecting to the device. Currently scans services.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        signals (DeviceConnectorSignals): The signals associated with this class.
        timeout (int): Max time allowed for a scan (in seconds).
        devices_found (dict): A list of found devices in address: name format.
    """

    def __init__(self):
        super(DeviceFinder, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DeviceFinderSignals()
        self.timeout = 10
        self.devices_found = {}

    def run(self):
        """Overrides the QRunnable implementation to start a device search thread."""
        self._logger.log('Starting new thread; searching for devices', Logger.DEBUG)

        try:
            agent = QBluetoothDeviceDiscoveryAgent()
            agent.setLowEnergyDiscoveryTimeout(1000)
            spy = QSignalSpy(agent.finished)
            agent.start()
            spy.wait(self.timeout * 1000)
            self.finished_search(agent.discoveredDevices())
        except Exception as error:
            self._logger.log('Exception encountered while searching for devices', Logger.ERROR)
            # self._logger.log(traceback.format_exc(), Logger.ERROR)
            self._logger.log(str(error), Logger.DEBUG)

        self._logger.log('Search complete, deleting thread', Logger.DEBUG)
        self.signals.searchComplete.emit(self.devices_found)

    def finished_search(self, devices):
        for device in devices:
            address = device.address().toString()
            name = device.name()
            self.devices_found[address] = name
            self._logger.log('Found bluetooth device with name: {} and address: {}'.format(name, address), Logger.DEBUG)
