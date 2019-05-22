from PyQt5.QtCore import pyqtSignal, QRunnable, QObject
from application.Logger import Logger
import bluetooth
import traceback


class PortTestSignals(QObject):
    testSuccessful = pyqtSignal(bool)

    def __init__(self):
        super(PortTestSignals, self).__init__()


class PortTest(QRunnable):
    """Class not used for demo, see SerialPortTest instead. """
    def __init__(self, host, port, uuid):
        super(PortTest, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = PortTestSignals()
        self.host = host
        self.port = port
        self.uuid = uuid

    def run(self):
        self._logger.log('Starting new thread; port test with {} on {}'.format(self.host, self.port), Logger.DEBUG)
        test_successful = False

        try:
            self._logger.log('Re-discovering devices to locate target', Logger.DEBUG)
            device_found = bluetooth.lookup_name(self.target_address)
            if device_found is None:
                self._logger.log('Could not re-discover target', Logger.DEBUG)
            else:
                self._logger.log('Re-discovered target', Logger.DEBUG)
                services = bluetooth.find_service(address=self.target_address)

                if len(services) > 0:
                    self._logger.log("Found {} services on {}".format(len(services), self.target_name), Logger.DEBUG)
                else:
                    self._logger.log("No services found", Logger.DEBUG)

                for service in services:
                    None

                test_successful = True
        except bluetooth.BluetoothError as error:
            self._logger.log(str(error), Logger.ERROR)
        except OSError:
            self._logger.log('Exception encountered while searching for devices', Logger.ERROR)
            self._logger.log(traceback.format_exc(), Logger.ERROR)

        self.signals.connectionComplete.emit(test_successful)
        self._logger.log('Deleting port test thread', Logger.DEBUG)
