import sys
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThreadPool
from application.Logger import Logger

if sys.platform.startswith('linux'):  # TODO: Revert this
    from controllers.connect_manager.DeviceFinderLinux import DeviceFinder
    from controllers.connect_manager.DeviceConnectorLinux import DeviceConnector
else:
    from controllers.connect_manager.DeviceFinder import DeviceFinder
    from controllers.connect_manager.DeviceConnector import DeviceConnector


class ConnectController(QObject):
    """ Controller class. Handles the core program logic and data transfer between its view and model counterparts.

       Args:
           model (QWidget): The controller's corresponding model.

       Parameters:
           connectionComplete (pyqtSignal): Signal emitted when connection has been completed.
           _model (QWidget): A reference to the passed model.
           _view (QWidget): A reference to this controller's corresponding view.
           name (str): The name of this class.
           _logger (Logger): Logging instance for this class.
           pool (QThreadPool): Global threadpool instance.
           device_connector (DeviceConnector): Device connection thread instance.
           attempts (int): No. of connection attempts left before failure considered.
       """

    connectionComplete = pyqtSignal(bool)  # TODO: Connection workflow needs to be decided

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.pool = QThreadPool.globalInstance()

        self.device_connector = DeviceConnector()
        self.device_connector.signals.connectionComplete.connect(self.connect_complete)
        self.device_connector.setAutoDelete(False)  # do not delete thread on return so more attempts can be made
        self.attempts = self._model.max_attempts

    def link_view(self, view):
        self._view = view

    @pyqtSlot()
    def search_button_clicked(self):
        """Slot implementation for when the search button is clicked or login is completed."""
        # disable the buttons while searching to prevent unknown behaviour
        self._view.toggle_search_button(value=False)
        self._view.toggle_connect_button(value=False)
        self._view.update_no_device(searching=True)

        device_finder = DeviceFinder()
        device_finder.signals.searchComplete.connect(self.search_complete)
        self.pool.start(device_finder)
        # print(self.pool.activeThreadCount())

    @pyqtSlot(dict)
    def search_complete(self, devices):
        """Slot implementation for when the device search has finished."""
        if len(devices) != 0:
            self._model.devices_found = devices.copy()
            self._view.update_devices(self._model.devices_found.values())
        else:
            self._logger.log("No bluetooth devices found", Logger.DEBUG)
            self._view.update_no_device(searching=False)
        self._view.toggle_search_button(True)  # suspect this will be useless once threading

    # TODO: multi-selection if pairing to multiple devices?
    @pyqtSlot()
    def selection_changed(self, selected):
        """Slot implementation for when the selected device in the list has changed."""
        if len(selected) != 0:
            self._logger.log("Device {} selected".format(self._view.get_text(selected[0].row())), Logger.DEBUG)
            self._view.toggle_connect_button(value=True)
        else:
            self._view.toggle_connect_button(value=False)

    @pyqtSlot()
    def connect_button_clicked(self, selected):
        """Slot implementation for when the user starts a connection attempt."""

        # disable the buttons while connecting to prevent unknown behaviour
        self._view.toggle_connect_button(value=False)  # TODO: unlock this properly
        self._view.toggle_search_button(value=False)

        devices = tuple(self._model.devices_found.items())
        self._model.target_device = devices[selected[0].row()]

        self._logger.log("Attempting to connect to {}".format(self._model.target_device[1]), Logger.DEBUG)
        self.device_connector.target_address = self._model.target_device[0]
        self.device_connector.target_name = self._model.target_device[1]
        self.pool.start(self.device_connector) # start connection thread

    @pyqtSlot(bool)
    def connect_complete(self, complete):
        """Slot implementation for when the  device connection attempt is complete."""
        self.attempts -= 1

        if not complete:
            # attempt another connection if counter has not reached zero:
            if self.attempts > 0:
                self._logger.log("Failed to connect; {} attempts remaining".format(self.attempts), Logger.DEBUG)
                self.pool.start(self.device_connector)
                # print(self.pool.activeThreadCount())
            else:
                self._logger.log("Out of attempts, could not connect to {}".format(self._model.target_device[1]),
                                 Logger.DEBUG)
        else:
            self._logger.log("Successfully connected to {}".format(self._model.target_device[1]), Logger.DEBUG)
            self.connectionComplete.emit(complete)

        self.attempts = self._model.max_attempts
        # re-enable buttons
        self._view.toggle_connect_button(value=True)
        self._view.toggle_search_button(value=True)
