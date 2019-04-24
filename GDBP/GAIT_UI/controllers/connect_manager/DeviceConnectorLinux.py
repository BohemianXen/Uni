from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, pyqtSlot
from application.Logger import Logger
from PyQt5.QtBluetooth import QLowEnergyController, QBluetoothDeviceInfo, QBluetoothDeviceDiscoveryAgent
import traceback
from PyQt5.QtTest import QSignalSpy



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
        self.timeout = 10
        self.target_address = ''
        self.target_name = ''

    def run(self):
        self._logger.log('Starting new thread; connecting with {}'.format(self.target_name), Logger.DEBUG)
        connection_complete = False
        try:
            self._logger.log('Re-discovering devices to locate target', Logger.DEBUG)
            agent = QBluetoothDeviceDiscoveryAgent()
            agent.setLowEnergyDiscoveryTimeout(1000)
            spy = QSignalSpy(agent.finished)
            agent.start()
            spy.wait(self.timeout * 1000)
            device = self.finished_search(agent.discoveredDevices())

            if device is not None and (device.coreConfigurations() and QBluetoothDeviceInfo.LowEnergyCoreConfiguration):
                self._logger.log('Confirmed {} is available and low energy profiled'.format(self.target_name),
                                 Logger.DEBUG)
                try:
                    self._logger.log('Creating low energy controller', Logger.DEBUG)
                    le_controller = QLowEnergyController.createCentral(device)
                    le_controller.setRemoteAddressType(QLowEnergyController.PublicAddress)
                    le_controller.error.connect(error_encountered)
                    le_controller.discoveryFinished.connect(discovery_done)
                    le_controller.connected.connect(connected)

                    self._logger.log('Connecting to device', Logger.DEBUG)
                    connection_spy = QSignalSpy(le_controller.connected)
                    le_controller.connectToDevice()
                    connection_spy.wait(self.timeout*1000)

                    self._logger.log('Discovering services', Logger.DEBUG)
                    service_scan_spy = QSignalSpy(le_controller.discoveryFinished)
                    le_controller.discoverServices()
                    service_scan_spy.wait(self.timeout*2*1000)

                    self._logger.log('Found services: {}'.format(le_controller.services()), Logger.DEBUG)
                    self._logger.log(le_controller.errorString(), Logger.DEBUG)

                    if le_controller.state() == QLowEnergyController.ConnectedState \
                            or le_controller.state() == QLowEnergyController.DiscoveredState:
                        connection_complete = True
                    else:
                        self._logger.log('Disconnecting from device', Logger.DEBUG)
                        le_controller.disconnectFromDevice()

                except Exception as _error:
                    self._logger.log(str(_error), Logger.DEBUG)
                    print(traceback.format_exc())

        except Exception as _error:
            self._logger.log('Exception encountered while attempting to connect to device', Logger.ERROR)
            self._logger.log(str(_error), Logger.ERROR)

        self.signals.connectionComplete.emit(connection_complete)
        # self._logger.log('Deleting connection thread', Logger.DEBUG)

    def finished_search(self, devices):
        for device in devices:
            address = device.address().toString()
            if address == self.target_address:
                return device

        return None

@pyqtSlot()
def discovery_done():
    print("Discovery done")
    #for service in controller.services():
    #    print(service.serviceClassToString())
    #    print(service.descriptorToString())

@pyqtSlot()
def error_encountered():
    print("Error!")

@pyqtSlot()
def connected():
    print("Connected!")
