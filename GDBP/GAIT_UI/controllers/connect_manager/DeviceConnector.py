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
    def __init__(self):
        super(DeviceConnector, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = DeviceConnectorSignals()
        self.target_address = ''
        self.target_name = ''

    def run(self):
        self._logger.log('Starting new thread; connecting with {}'.format(self.target_name), Logger.DEBUG)
        connection_complete = False
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
                    self._logger.log("Service Name: {}".format(service["name"]), Logger.DEBUG)
                    self._logger.log("    Host:        {}".format(service["host"]), Logger.DEBUG)
                    self._logger.log("    Description: {}".format(service["description"]), Logger.DEBUG)
                    self._logger.log("    Provided By: {}".format(service["provider"]), Logger.DEBUG)
                    self._logger.log("    Protocol:    {}".format(service["protocol"]), Logger.DEBUG)
                    self._logger.log("    Channel/PSM: {}".format(service["port"]), Logger.DEBUG)
                    self._logger.log("    Service Classes: {}".format(service["service-classes"]), Logger.DEBUG)
                    self._logger.log("    Profiles:    {}".format(service["profiles"]), Logger.DEBUG)
                    self._logger.log("    Service ID:  {}".format(service["service-id"]), Logger.DEBUG)

                connection_complete = True
        except bluetooth.BluetoothError as error:
            self._logger.log(str(error), Logger.ERROR)
        except OSError:
            self._logger.log('Exception encountered while searching for devices', Logger.ERROR)
            self._logger.log(traceback.format_exc(), Logger.ERROR)

        self.signals.connectionComplete.emit(connection_complete)
        self._logger.log('Deleting connection thread', Logger.DEBUG)
