from PyQt5.QtCore import pyqtSignal, QRunnable, QObject
from application.Logger import Logger
import bluetooth
import traceback


class DeviceConnectorSignals(QObject):
    connectionComplete = pyqtSignal(bool)

    def __init__(self):
        super(DeviceConnectorSignals, self).__init__()


# TODO: Add checks for own bluetooth chip
class DeviceConnector(QRunnable):
    def __init__(self, target_address, target_name):
        super(DeviceConnector, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DeviceConnectorSignals()
        self._target_address = target_address
        self._target_name = target_name

    def run(self):
        self._logger.log('Starting new thread; connecting with {}'.format(self._target_name), Logger.DEBUG)
        connection_complete = False
        try:
            device_found = bluetooth.lookup_name(self._target_address)
            if device_found is None:
                print('Uh oh')
            else:
                print('Yay')
                connection_complete = True
        except bluetooth.BluetoothError as error:
            self._logger.log(str(error), Logger.ERROR)
        except OSError:
            self._logger.log('Exception encountered while searching for devices', Logger.ERROR)
            self._logger.log(traceback.format_exc(), Logger.ERROR)

        self.signals.connectionComplete.emit(connection_complete)
        self._logger.log('Deleting connection thread', Logger.DEBUG)
