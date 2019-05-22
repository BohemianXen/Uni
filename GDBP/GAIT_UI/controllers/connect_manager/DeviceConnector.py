from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, QElapsedTimer
from application.Logger import Logger
import bluetooth
import traceback


class DeviceConnectorSignals(QObject):
    connectionComplete = pyqtSignal(bool)

    def __init__(self):
        super(DeviceConnectorSignals, self).__init__()


# TODO: Add checks for own bluetooth chip
class DeviceConnector(QRunnable):
    """PyBluez class for connecting to the device. Currently scans services.

    Parameters:
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        signals (DeviceConnectorSignals): The signals associated with this class.
        target_address (str): MAC Address of selected device.
        target_name (str): Name of selected device.
    """

    def __init__(self):
        super(DeviceConnector, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DeviceConnectorSignals()
        self.target_address = ''
        self.target_name = ''

    def run(self):
        """Overrides the QRunnable implementation to start a device connection thread."""
        self._logger.log('Starting new thread; connecting with {}'.format(self.target_name), Logger.DEBUG)
        connection_complete = False

        try:
            self._logger.log('Re-discovering devices to locate target', Logger.DEBUG)
            device_found = bluetooth.lookup_name(self.target_address)
            if device_found is None:
                self._logger.log('Could not re-discover target', Logger.DEBUG)
            else:
                self._logger.log('Re-discovered target, scanning services', Logger.DEBUG)

                timer = QElapsedTimer()
                timer.start()
                services = bluetooth.find_service(address=self.target_address)
                scan_time = timer.elapsed()
                self._logger.log('Completed scan in {} ms'.format(scan_time), Logger.DEBUG)

                if len(services) > 0:
                    self._logger.log("Found {} services on {}".format(len(services), self.target_name), Logger.DEBUG)
                    connection_complete = True
                else:
                    self._logger.log("No services found", Logger.DEBUG)

                for service in services:
                    self._logger.log("Service Name: {}".format(service["name"]), Logger.DEBUG)
                    self._logger.log("    Host:        {}".format(service["host"]), Logger.DEBUG)
                    self._logger.log("    Description: {}".format(service["description"]), Logger.DEBUG)
                    self._logger.log("    Provided By: {}".format(service["provider"]), Logger.DEBUG)
                    self._logger.log("    Protocol:    {}".format(service["protocol"]), Logger.DEBUG)
                    self._logger.log("    Channel/PSM: {}".format(service["port"]), Logger.DEBUG)
                    self._logger.log("    Service Classes: {}".format(service["service-classes"]), Logger.DEBUG)
                    self._logger.log("    Profiles:    {}".format(service["profiles"]), Logger.DEBUG)
                    self._logger.log("    Service ID:  {}".format(service["service-id"]), Logger.DEBUG)

        except bluetooth.BluetoothError as error:
            self._logger.log(str(error), Logger.ERROR)
        except OSError:
            self._logger.log('Exception encountered while searching for devices', Logger.ERROR)
            self._logger.log(traceback.format_exc(), Logger.ERROR)

        self.signals.connectionComplete.emit(connection_complete)
        self._logger.log('Deleting connection thread', Logger.DEBUG)
