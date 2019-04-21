from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from views.ui_files.connect_view_ui import Ui_ConnectView
from application.Logger import Logger


class ConnectView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_ConnectView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)
        self._selected_device = self._ui.devicesListWidget.selectedIndexes()
        self.no_device = QListWidgetItem(self._ui.devicesListWidget.item(0))

        # connect buttons to their respective controller slots
        self._ui.searchButton.clicked.connect(lambda: self._controller.search_button_clicked())
        self._ui.connectButton.clicked.connect(lambda: self._controller.connect_button_clicked(self._selected_device))
        self._ui.devicesListWidget.clicked.connect(
            lambda: self._controller.selection_changed(self._ui.devicesListWidget.selectedIndexes()))

    def toggle_search_button(self, value):
        self._ui.searchButton.setEnabled(value)

    def toggle_connect_button(self, value):
        self._ui.connectButton.setEnabled(value)

    def update_devices(self, device):
        self.update_no_device()
        self._logger.log('Adding {} to found devices list'.format(device), Logger.DEBUG)
        self._ui.devicesListWidget.addItem(self.create_new_item(device))

    def create_new_item(self, text):
        new_item = QListWidgetItem(text)
        new_item.setTextAlignment(Qt.AlignCenter)
        return new_item

    def update_no_device(self):
        self._logger.log('Updating no devices text', Logger.DEBUG)

        if self.get_text(0) == self.no_device.text():
            self._ui.devicesListWidget.takeItem(0)
        else:
            for index in range(self._ui.devicesListWidget.count()):
                self._ui.devicesListWidget.takeItem(index)

            self._ui.devicesListWidget.addItem(self.no_device)

    def get_text(self, index):
        if type(index) is int:
            return self._ui.devicesListWidget.item(index).text()
        else:
            text = [self._ui.devicesListWidget.item(i).text() for i in range(self._ui.devicesListWidget.count())]
            return text
