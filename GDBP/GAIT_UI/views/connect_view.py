from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from views.ui_files.connect_view_ui import Ui_ConnectView
from application.Logger import Logger


class ConnectView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

      Args:
          controller (QWidget): The view's corresponding controller; that which manipulates this view

      Parameters:
          _controller (QWidget): A reference to the passed controller
          _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction
          name (str): The name of this class
          _logger (Logger): Logging instance for this class
          no_device (QListWidgetItem): Top level item that holds the no device found message
          searching_status (QListWidgetItem): Top level item that holds the searching for devices message
    """

    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_ConnectView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self.no_device = QListWidgetItem(self._ui.devicesListWidget.item(0))
        self.searching_status = QListWidgetItem(self._ui.devicesListWidget.item(1))
        self._ui.devicesListWidget.takeItem(1)

        # connect buttons to their respective controller slots
        self._ui.searchButton.clicked.connect(lambda: self._controller.search_button_clicked())
        self._ui.connectButton.clicked.connect(
            lambda: self._controller.connect_button_clicked(self._ui.devicesListWidget.selectedIndexes()))
        self._ui.devicesListWidget.clicked.connect(
            lambda: self._controller.selection_changed(self._ui.devicesListWidget.selectedIndexes()))

    def toggle_search_button(self, value):
        self._ui.searchButton.setEnabled(value)

    def toggle_connect_button(self, value):
        self._ui.connectButton.setEnabled(value)

    def update_devices(self, devices):
        self.remove_all_items()
        for device in devices:
            self._logger.log('Adding {} to found devices list'.format(device), Logger.DEBUG)
            self._ui.devicesListWidget.addItem(self.create_new_item(device))

    def update_no_device(self, searching):
        self._logger.log('Updating status text', Logger.DEBUG)
        self.remove_all_items()
        new_message = self.searching_status if searching else self.no_device
        self._ui.devicesListWidget.addItem(new_message)

    @staticmethod
    def create_new_item(text):
        new_item = QListWidgetItem(text)
        new_item.setTextAlignment(Qt.AlignCenter)
        return new_item

    def remove_all_items(self):
        for index in range(self._ui.devicesListWidget.count()):
            self._ui.devicesListWidget.takeItem(0)

    def get_text(self, index):
        if type(index) is int:
            return self._ui.devicesListWidget.item(index).text()
        else:
            text = [self._ui.devicesListWidget.item(i).text() for i in range(self._ui.devicesListWidget.count())]
            return text
